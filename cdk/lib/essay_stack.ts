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
import * as logs from 'aws-cdk-lib/aws-logs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as s3_notifications from 'aws-cdk-lib/aws-s3-notifications';
import * as sqs from 'aws-cdk-lib/aws-sqs';

import * as s3_deployment from 'aws-cdk-lib/aws-s3-deployment';
export interface EssayStackProps extends cdk.StackProps {
}

export class EssayStack extends cdk.Stack {
  // Declare the OAI as a class property
  public readonly originAccessIdentity: cloudfront.OriginAccessIdentity;

  constructor(scope: Construct, id: string, props: EssayStackProps) {
    super(scope, id, props);
    this.originAccessIdentity = new cloudfront.OriginAccessIdentity(this, 'OAI');

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
    this.setupS3EventProcessing(s3Bucket);
  }

  private setupS3EventProcessing(s3Bucket: s3.Bucket): void {
    const s3EventHandlerLambda = this.createS3EventHandlerLambda();
    const topicQueue = this.createTopicQueue();
  
    s3Bucket.grantRead(s3EventHandlerLambda);
    topicQueue.grantSendMessages(s3EventHandlerLambda);
    s3EventHandlerLambda.addEnvironment('SQS_QUEUE_URL', topicQueue.queueUrl);
  
    s3Bucket.addEventNotification(s3.EventType.OBJECT_CREATED, new s3_notifications.LambdaDestination(s3EventHandlerLambda));
  }
  
  private createS3EventHandlerLambda(): lambda.Function {
    return new lambda.Function(this, 'S3EventHandlerFunction', {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: 's3_event_handler.lambda_handler',
      code: lambda.Code.fromAsset('../infra/recurringTasks'),
    });
  }

  private createTopicQueue(): sqs.Queue {
    return new sqs.Queue(this, 'TopicQueue');
  }
  
  outputApiUrl(api: apigateway.RestApi) {
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: `https://${api.restApiId}.execute-api.${this.region}.amazonaws.com/`,
    });
  }
  createS3Bucket(domainName: string) {

    const bucket = new s3.Bucket(this, 'StaticSiteBucket', {
      bucketName: domainName, // Use the same name as your existing bucket if you want to keep the same domain name
      websiteIndexDocument: 'index.html',
      removalPolicy: cdk.RemovalPolicy.DESTROY, // Update this based on your requirements
    });
    bucket.grantRead(this.originAccessIdentity);

    // CORS configuration to allow all requests from everywhere
    bucket.addCorsRule({
      allowedMethods: [s3.HttpMethods.PUT, s3.HttpMethods.POST, s3.HttpMethods.GET, s3.HttpMethods.HEAD],
      allowedOrigins: ['*'],
      allowedHeaders: ['*'],
    });
    
    new s3_deployment.BucketDeployment(this, 'DeployAssets', {
      sources: [s3_deployment.Source.asset('../frontend/build'), s3_deployment.Source.asset('../content')],
      destinationBucket: bucket
    });
    return bucket;
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
            originAccessIdentity: this.originAccessIdentity
          },
          behaviors: [
            {
              pathPattern: '/blog/*',
              allowedMethods: cloudfront.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
              forwardedValues: {
                queryString: true,
              },
              defaultTtl: cdk.Duration.seconds(0),
              compress: true,
              isDefaultBehavior: false, // Set isDefaultBehavior to false for the blog post behavior
            },
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
            {
              pathPattern: '/sitemap.xml', // add this line to match requests to /sitemap.xml
              allowedMethods: cloudfront.CloudFrontAllowedMethods.GET_HEAD_OPTIONS,
              defaultTtl: cdk.Duration.seconds(0),
              forwardedValues: {
                queryString: false,
              },
              compress: true,
            },
          ],
        }
      ],
      viewerCertificate: cloudfront.ViewerCertificate.fromAcmCertificate(sslCertificate, {
        aliases: [domainName, `www.${domainName}`],
      }),
      errorConfigurations: [
        {
          errorCode: 404,
          responseCode: 200,
          responsePagePath: '/index.html',
        },
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
    new route53.CnameRecord(this, 'GoogleCnameRecord', {
      zone: hostedZone,
      recordName: 'qshtfjw6qnm6',
      domainName: 'gv-lp65xxcad3glo6.dv.googlehosted.com',
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
      // deployOptions: {
      //   accessLogDestination: new apigateway.LogGroupLogDestination(new logs.LogGroup(this, 'ApiAccessLogs', {
      //     logGroupName: `/aws/api-gateway/pixelpen`,
      //     retention: logs.RetentionDays.ONE_WEEK,
      //     removalPolicy: cdk.RemovalPolicy.DESTROY
      //   })),
      //   accessLogFormat: apigateway.AccessLogFormat.jsonWithStandardFields(),
      // }
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
