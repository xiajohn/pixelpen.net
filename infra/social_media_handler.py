import sys
sys.path.insert(0, 'social_dependency')
import traceback
from recurringTasks.social_media.facebookCreator import createFacebookPost

import json
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Received Event: {json.dumps(event)}")
    
    
    try:
        createFacebookPost()
    except Exception as e:
        print("Error occurred:", str(e))
        print(traceback.format_exc())

    return {
        "statusCode": 200,
        "body": json.dumps("Successfully processed EventBridge event."),
    }
