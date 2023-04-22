import * as cdk from 'aws-cdk-lib';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';
import * as ses from 'aws-cdk-lib/aws-ses';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as logs from 'aws-cdk-lib/aws-logs';

export class EssayStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const domainName = 'pixelpen.net';
    const s3Bucket = this.createS3Bucket(domainName);
    const hostedZone = this.createHostedZone(domainName);
    const sslCertificate = this.createSSLCertificate(domainName, hostedZone);
    const identity = this.createSESEmailIdentity(hostedZone);
    this.verifySESEmailAddresses();
    const distribution = this.createCloudFrontDistribution(s3Bucket, sslCertificate, domainName);
    this.createRoute53Records(hostedZone, distribution, domainName);
    const sesSendEmailPolicy = this.createSESSendEmailPolicy();
    const myLambda = this.createLambdaFunction();
    const api = this.createApiGateway(myLambda);
    this.addApiGatewayResources(myLambda, api);
    this.outputApiUrl(api);
  }
  outputApiUrl(api: apigateway.RestApi) {
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: `https://${api.restApiId}.execute-api.${this.region}.amazonaws.com/`,
    });
  }
  createS3Bucket(domainName: string) {
    return s3.Bucket.fromBucketName(this, 'ImportedBucket', domainName);
  }

  createHostedZone(domainName: string) {
    return new route53.HostedZone(this, 'HostedZone', {
      zoneName: domainName,
    });
  }

  createSSLCertificate(domainName: string, hostedZone: route53.HostedZone) {
    return new acm.DnsValidatedCertificate(this, 'SSLCertificate', {
      domainName: domainName,
      subjectAlternativeNames: [`www.${domainName}`],
      hostedZone: hostedZone,
      region: 'us-east-1',
    });
  }

  createSESEmailIdentity(hostedZone: route53.HostedZone) {
    return new ses.EmailIdentity(this, 'Identity', {
      identity: ses.Identity.publicHostedZone(hostedZone)
    });
  }

  verifySESEmailAddresses() {
    new ses.CfnEmailIdentity(this, 'XiajohnEmail', {
      emailIdentity: 'xiajohn@hotmail.com',
    });

    new ses.CfnEmailIdentity(this, 'MeszterEmail', {
      emailIdentity: 'meszter.17@gmail.com',
    });
  }
  createCloudFrontDistribution(s3Bucket: s3.IBucket, sslCertificate: acm.DnsValidatedCertificate, domainName: string) {
    return new cloudfront.CloudFrontWebDistribution(this, 'CloudFrontDistribution', {
      originConfigs: [
        {
          s3OriginSource: {
            s3BucketSource: s3Bucket,
          },
          behaviors: [
            {
              defaultTtl: cdk.Duration.seconds(0),
              allowedMethods: cloudfront.CloudFrontAllowedMethods.ALL,
              forwardedValues: {
                queryString: true,
                headers: [
                  'Access-Control-Request-Headers',
                  'Access-Control-Request-Method',
                  'Origin',
                ],
              },
              isDefaultBehavior: true,
              viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            },
          ],
        },
      ],
      viewerCertificate: cloudfront.ViewerCertificate.fromAcmCertificate(sslCertificate, {
        aliases: [domainName, `www.${domainName}`],
      }),
      errorConfigurations: [
        {
          errorCode: 403,
          responseCode: 200,
          responsePagePath: '/index.html',
        },
      ],
    });
  }
  createRoute53Records(hostedZone: route53.HostedZone, distribution: cloudfront.CloudFrontWebDistribution, domainName: string) {
    new route53.ARecord(this, 'ARecord', {
      zone: hostedZone,
      target: route53.RecordTarget.fromAlias(new targets.CloudFrontTarget(distribution)),
    });

    new route53.CnameRecord(this, 'CnameRecord', {
      zone: hostedZone,
      recordName: `www.${domainName}`,
      domainName: distribution.distributionDomainName,
    });
  }

  createSESSendEmailPolicy() {
    return new iam.ManagedPolicy(this, 'SESSendEmailPolicy', {
      statements: [
        new iam.PolicyStatement({
          actions: ['ses:SendEmail', 'ses:SendRawEmail'],
          resources: ['*'],
        }),
      ],
    });
  }

  createLambdaFunction() {
    const lambdaLoggingRole = new iam.Role(this, 'LambdaLoggingRole', {
      assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
    });
    lambdaLoggingRole.addToPolicy(
      new iam.PolicyStatement({
        actions: ['ses:SendEmail', 'ses:SendRawEmail'],
        resources: ['*'],
      }),
    );

    lambdaLoggingRole.addManagedPolicy(
      iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
    );

    return new lambda.Function(this, 'MyLambdaFunction', {
      runtime: lambda.Runtime.NODEJS_14_X,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('../server/dist'),
      role: lambdaLoggingRole,
      environment: {
        CURRENT_TIMESTAMP: new Date().toISOString(),
      },
      timeout: cdk.Duration.seconds(20),
      description: `My Lambda function. Last updated on ${new Date().toISOString()}.`,
    });
  }

  createApiGateway(myLambda: lambda.Function) {
    return new apigateway.RestApi(this, 'MyApiGateway', {
      restApiName: 'My Service',
      description: 'API Gateway for My Service',
      policy: new iam.PolicyDocument({
        statements: [
          new iam.PolicyStatement({
            actions: ['execute-api:Invoke'],
            resources: ['*'],
            effect: iam.Effect.ALLOW,
            principals: [new iam.ArnPrincipal('*')],
          }),
        ],
      }),
      defaultMethodOptions: {
        authorizationType: apigateway.AuthorizationType.NONE,
      },
      deployOptions: {
        accessLogDestination: new apigateway.LogGroupLogDestination(new logs.LogGroup(this, 'ApiAccessLogs', {
          logGroupName: `/aws/api-gateway/pixelpen`,
          retention: logs.RetentionDays.ONE_WEEK,
        })),
        accessLogFormat: apigateway.AccessLogFormat.jsonWithStandardFields(),
      }
    });
  }

  addApiGatewayResources(myLambda: lambda.Function, api: apigateway.RestApi) {
    const lambdaIntegration = new apigateway.LambdaIntegration(myLambda);

    const resources = ['generate-essay', 'send-email'];

    const mockIntegration = new apigateway.MockIntegration({
      integrationResponses: [
        {
          statusCode: '200',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Headers': "'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token'",
            'method.response.header.Access-Control-Allow-Origin': "'*'",
            'method.response.header.Access-Control-Allow-Methods': "'OPTIONS,GET,POST'",
            'method.response.header.Access-Control-Allow-Credentials': "'false'",
          },
        },
      ],
      passthroughBehavior: apigateway.PassthroughBehavior.NEVER,
      requestTemplates: {
        'application/json': '{"statusCode": 200}',
      },
    });

    const methodOptions = {
      methodResponses: [
        {
          statusCode: '200',
          responseParameters: {
            'method.response.header.Access-Control-Allow-Headers': true,
            'method.response.header.Access-Control-Allow-Origin': true,
            'method.response.header.Access-Control-Allow-Methods': true,
            'method.response.header.Access-Control-Allow-Credentials': true,
          },
        },
      ],
    };

    resources.forEach((resourceName) => {
      const resource = api.root.addResource(resourceName);
      resource.addMethod('POST', lambdaIntegration);
      resource.addMethod('GET', lambdaIntegration);
      resource.addMethod('OPTIONS', mockIntegration, methodOptions);
    });
  }


  addApiGatewayOutput(api: apigateway.RestApi) {
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: `https://${api.restApiId}.execute-api.${this.region}.amazonaws.com/`,
    });
  }

  // Call the refactored functions in the constructor


}
