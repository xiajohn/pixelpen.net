import * as cdk from 'aws-cdk-lib';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import * as acm from 'aws-cdk-lib/aws-certificatemanager';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';
import * as ses from 'aws-cdk-lib/aws-ses';
import * as iam from 'aws-cdk-lib/aws-iam'; // Import the IAM module
import * as cloudfront from 'aws-cdk-lib/aws-cloudfront'; // Import the CloudFront module
import * as apigateway from 'aws-cdk-lib/aws-apigateway'; // Import the API Gateway module
import * as lambda from 'aws-cdk-lib/aws-lambda'; // Import the Lambda module
import * as logs from 'aws-cdk-lib/aws-logs';
export class EssayStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // Your custom domain
    const domainName = 'pixelpen.net';


    // Import your existing S3 bucket
    const s3Bucket = s3.Bucket.fromBucketName(this, 'ImportedBucket', domainName);

    // Create a Route 53 Hosted Zone
    const hostedZone = new route53.HostedZone(this, 'HostedZone', {
      zoneName: domainName,
    });

    // Request an SSL certificate from ACM
    const sslCertificate = new acm.DnsValidatedCertificate(this, 'SSLCertificate', {
      domainName: domainName,
      subjectAlternativeNames: [`www.${domainName}`], // Add the www subdomain here
      hostedZone: hostedZone,
      region: 'us-east-1', // ACM certificates must be in the us-east-1 region for CloudFront
    });


    const identity = new ses.EmailIdentity(this, 'Identity', {
      identity: ses.Identity.publicHostedZone(hostedZone)
    });

    // Verify additional email addresses
    new ses.CfnEmailIdentity(this, 'XiajohnEmail', {
      emailIdentity: 'xiajohn@hotmail.com',
    });

    new ses.CfnEmailIdentity(this, 'MeszterEmail', {
      emailIdentity: 'meszter.17@gmail.com',
    });

    // Create a CloudFront distribution with the SSL certificate
    const distribution = new cloudfront.CloudFrontWebDistribution(this, 'CloudFrontDistribution', {
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
              viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS, // Automatically redirect HTTP to HTTPS
            },
          ],
        },
      ],
      viewerCertificate: cloudfront.ViewerCertificate.fromAcmCertificate(sslCertificate, {
        aliases: [domainName, `www.${domainName}`],
      }),
    });

    // Create a ManagedPolicy with the necessary permissions for sending emails
    const sesSendEmailPolicy = new iam.ManagedPolicy(this, 'SESSendEmailPolicy', {
      statements: [
        new iam.PolicyStatement({
          actions: ['ses:SendEmail', 'ses:SendRawEmail'],
          resources: ['*'],
        }),
      ],
    });
    // Create the A Record (Apex domain)
    new route53.ARecord(this, 'ARecord', {
      zone: hostedZone,
      target: route53.RecordTarget.fromAlias(new targets.CloudFrontTarget(distribution)),
    });

    // Create the CNAME Record (www subdomain)
    new route53.CnameRecord(this, 'CnameRecord', {
      zone: hostedZone,
      recordName: `www.${domainName}`,
      domainName: distribution.distributionDomainName,
    });


    // Create an IAM role for Lambda logging
const lambdaLoggingRole = new iam.Role(this, 'LambdaLoggingRole', {
  assumedBy: new iam.ServicePrincipal('lambda.amazonaws.com'),
});

// Attach the AWS managed policy "AWSLambdaBasicExecutionRole" to the role
lambdaLoggingRole.addManagedPolicy(
  iam.ManagedPolicy.fromAwsManagedPolicyName('service-role/AWSLambdaBasicExecutionRole')
);

const myLambda = new lambda.Function(this, 'MyLambdaFunction', {
  runtime: lambda.Runtime.NODEJS_14_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('../server/dist'),
  role: lambdaLoggingRole,
  environment: {
    CURRENT_TIMESTAMP: new Date().toISOString(),
  },
  timeout: cdk.Duration.seconds(10),
  description: `My Lambda function. Last updated on ${new Date().toISOString()}.`,
});


    // Create an API Gateway
    const api = new apigateway.RestApi(this, 'MyApiGateway', {
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

    // Connect the Lambda function to the API Gateway
    const lambdaIntegration = new apigateway.LambdaIntegration(myLambda);
    
    
    
    // Create a deployment and stage for the API Gateway
    const deployment = new apigateway.Deployment(this, 'MyApiDeployment', {
      api: api
    });


    const essay = api.root.addResource('generate-essay');
    essay.addMethod('POST', lambdaIntegration);
// Add a GET method to the resource
essay.addMethod('GET', lambdaIntegration);
  // Add MockIntegration for the OPTIONS method
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

// Add the OPTIONS method to the essay resource
essay.addMethod('OPTIONS', mockIntegration, {
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
});
    // Add the API Gateway URL to the stack output
    new cdk.CfnOutput(this, 'ApiUrl', {
      value: `https://${api.restApiId}.execute-api.${this.region}.amazonaws.com/`,
    });

    
  }
}
