import * as cdk from 'aws-cdk-lib';
import * as route53 from 'aws-cdk-lib/aws-route53';
import * as targets from 'aws-cdk-lib/aws-route53-targets';
import * as s3 from 'aws-cdk-lib/aws-s3';
import { Construct } from 'constructs';
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

    // Create the A Record (Apex domain)
    new route53.ARecord(this, 'ARecord', {
      zone: hostedZone,
      target: route53.RecordTarget.fromAlias(new targets.BucketWebsiteTarget(s3Bucket)),
    });

    // Create the CNAME Record (www subdomain)
    new route53.CnameRecord(this, 'CnameRecord', {
      zone: hostedZone,
      recordName: `www.${domainName}`,
      domainName: s3Bucket.bucketWebsiteDomainName,
    });
  }
}
