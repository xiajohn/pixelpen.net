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
import * as events from 'aws-cdk-lib/aws-events';
import * as eventtargets from 'aws-cdk-lib/aws-events-targets';
import * as s3_deployment from 'aws-cdk-lib/aws-s3-deployment';
import * as dotenv from 'dotenv';

dotenv.config();
export interface EssayStackProps extends cdk.StackProps {
}

export class EssayStack extends cdk.Stack {
  public readonly originAccessIdentity: cloudfront.OriginAccessIdentity;
  private commonExcludeDirectories: string[] = ['tmp', 'tmp/*', 'video', 'video/*', 'common/video', 'common/video/*', 'generated', 'generated/*', 'blogPipeline', 'blogPipeline/*', '__pycache__', '__pycache__/*', 'test', 'test/*', 'user_input.json', 'run.py', '.gitignore', '.env'];
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
    this.setupEventProcessing(s3Bucket);
  }

  private setupEventProcessing(s3Bucket: s3.Bucket): void {
    const lambdas = this.createEventHandlerLambda();

    const dailyRule = new events.Rule(this, 'DailyRule', {
      schedule: events.Schedule.cron({ minute: '0', hour: '13' }), // This schedules the event at 13:00 (or 1:00 PM) UTC every day
    });

    dailyRule.addTarget(new eventtargets.LambdaFunction(lambdas[0], { retryAttempts: 1 }));
    dailyRule.addTarget(new eventtargets.LambdaFunction(lambdas[1], { retryAttempts: 1 }));
  }

  private createEventHandlerLambda(): lambda.Function[] {
    const pillowLayer = lambda.LayerVersion.fromLayerVersionArn(this, 'pillowLayer', 'arn:aws:lambda:us-west-1:770693421928:layer:Klayers-p39-pillow:1');
    const requestLayer = lambda.LayerVersion.fromLayerVersionArn(this, 'requestLayer', 'arn:aws:lambda:us-west-1:770693421928:layer:Klayers-p39-requests:13');
    const numpyLayer = lambda.LayerVersion.fromLayerVersionArn(this, 'numpyLayer', 'arn:aws:lambda:us-west-1:770693421928:layer:Klayers-p39-numpy:12');
    const pandas = lambda.LayerVersion.fromLayerVersionArn(this, 'pandas', 'arn:aws:lambda:us-west-1:770693421928:layer:Klayers-p39-pandas:14');
    const matplotlib = lambda.LayerVersion.fromLayerVersionArn(this, 'matplotlib', 'arn:aws:lambda:us-west-1:770693421928:layer:Klayers-p39-matplotlib:1');

    const eventLambdaExcludeDirectories = this.commonExcludeDirectories.concat(['social_dependency', 'social_dependency/*', 'common/makememe', 'common/makememe/*']);
    const eventLambda = this.createLambda('S3EventHandlerFunction', 'email_handler.lambda_handler', eventLambdaExcludeDirectories, [requestLayer]);

    const socialEventLambdaExcludeDirectories = this.commonExcludeDirectories.concat(['dependency', 'dependency/*']);
    const socialEventLambda = this.createLambda('socialHandlerFunction', 'social_media_handler.lambda_handler', socialEventLambdaExcludeDirectories, [pillowLayer, numpyLayer, requestLayer]);

    return [eventLambda, socialEventLambda];
  }

  private createLambda(id: string, handler: string, excludeDirectories: string[], layerList: lambda.ILayerVersion[]): lambda.Function {
    const lambdaFunction = new lambda.Function(this, id, {
      runtime: lambda.Runtime.PYTHON_3_9,
      handler: handler,
      environment: {
        OPENAI_API_KEY: process.env.OPENAI_API_KEY!,
        FACEBOOK_ACCESS_KEY: process.env.FACEBOOK_ACCESS_KEY!,
        ...(id === 'S3EventHandlerFunction' && {SENDGRID_API_KEY: process.env.SENDGRID_API_KEY!, GOOGLE_SEARCH_API_KEY: process.env.GOOGLE_SEARCH_API_KEY!})
      },
      code: lambda.Code.fromAsset('../infra', {
        exclude: excludeDirectories
      }),
      timeout: cdk.Duration.seconds(id === 'S3EventHandlerFunction' ? 760 : 560),
      memorySize: 1024
    });

    lambdaFunction.addLayers(...layerList);
    lambdaFunction.addPermission('AllowEventBridge', {
      principal: new iam.ServicePrincipal('events.amazonaws.com'),
    });

    return lambdaFunction;
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
      destinationBucket: bucket,
      memoryLimit: 256
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
    new route53.CnameRecord(this, 'zoho', {
      zone: hostedZone,
      recordName: 'zb60703553',
      domainName: 'zmverify.zoho.com',
    });
    new route53.CnameRecord(this, 'CnameRecord', {
      zone: hostedZone,
      recordName: `www.${domainName}`,
      domainName: distribution.distributionDomainName,
    });
    // MX Records
    new route53.MxRecord(this, 'ZohoMxRecord', {
      zone: hostedZone,
      recordName: domainName,
      values: [
        {
          priority: 10,
          hostName: 'mx.zoho.com',
        },
        {
          priority: 20,
          hostName: 'mx2.zoho.com',
        },
        {
          priority: 50,
          hostName: 'mx3.zoho.com',
        },
      ],
      ttl: cdk.Duration.minutes(5),
    });

    // SPF Record
    new route53.TxtRecord(this, 'ZohoSpfRecord', {
      zone: hostedZone,
      recordName: domainName,
      values: ['v=spf1 include:zoho.com ~all'],
      ttl: cdk.Duration.minutes(5),
    });

    // DKIM Record
    new route53.TxtRecord(this, 'ZohoDkimRecord', {
      zone: hostedZone,
      recordName: `zmail._domainkey.${domainName}`,
      values: [
        'v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCtsSfRSeXhmvKjDzKFZRTPxpukFnZHS3ZGOQUmHdnj++z2X3NMW2O1Qvtw7rJRaDEE5laW7SjTKSS5NzNEqYYzQAXVKUeEAIAnmiHFrzNMkmgP7Fowd0BM1EQ1xzDsL4Y0TndXH78Ny/RilCCKuq0iOtOR8PTRB7uBWkYdDiZ2KwIDAQAB',
      ],
      ttl: cdk.Duration.minutes(5),
    });
    // CNAME Records
    new route53.CnameRecord(this, 'SendGridCnameRecord1', {
      zone: hostedZone,
      recordName: 'url5640.' + domainName,
      domainName: 'sendgrid.net',
      ttl: cdk.Duration.minutes(5),
    });

    new route53.CnameRecord(this, 'SendGridCnameRecord2', {
      zone: hostedZone,
      recordName: '34162867.' + domainName,
      domainName: 'sendgrid.net',
      ttl: cdk.Duration.minutes(5),
    });

    new route53.CnameRecord(this, 'SendGridCnameRecord3', {
      zone: hostedZone,
      recordName: 'em9434.' + domainName,
      domainName: 'u34162867.wl118.sendgrid.net',
      ttl: cdk.Duration.minutes(5),
    });

    new route53.CnameRecord(this, 'SendGridCnameRecord4', {
      zone: hostedZone,
      recordName: 's1._domainkey.' + domainName,
      domainName: 's1.domainkey.u34162867.wl118.sendgrid.net',
      ttl: cdk.Duration.minutes(5),
    });

    new route53.CnameRecord(this, 'SendGridCnameRecord5', {
      zone: hostedZone,
      recordName: 's2._domainkey.' + domainName,
      domainName: 's2.domainkey.u34162867.wl118.sendgrid.net',
      ttl: cdk.Duration.minutes(5),
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
}
