import sys
sys.path.insert(0, 'dependency')
from recurringTasks.email.main import sendEmails
from recurringTasks.social_media.facebookCreator import createFacebookPost

import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received Event: {json.dumps(event)}")

    sendEmails()

    return {
        "statusCode": 200,
        "body": json.dumps("Successfully processed EventBridge event."),
    }
