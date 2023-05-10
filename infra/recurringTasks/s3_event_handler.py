import json
import boto3
import os

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

def lambda_handler(event, context):
    object_key = event['Records'][0]['s3']['object']['key']
    new_folder_name = object_key.split('/')[0]
    sqs_queue_url = os.environ['SQS_QUEUE_URL']
    sqs.send_message(
        QueueUrl=sqs_queue_url,
        MessageBody=json.dumps({'folder_name': new_folder_name})
    )
