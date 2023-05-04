from aiohttp import ClientError
import boto3
from dotenv import load_dotenv
import os
import json
import logging

load_dotenv()

def send_message(queue, message_body, message_attributes=None):
    if not message_attributes:
        message_attributes = {}

    try:
        response = queue.send_message(
            MessageBody=message_body,
            MessageAttributes=message_attributes
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            print("Message published.")
        
    except ClientError as error:
        logging.exception("Send message failed: %s", message_body)
        raise error
    else:
        return response


if __name__ == "__main__":
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_access_token = os.getenv("AWS_ACCESS_TOKEN")
    aws_region_name = os.getenv("AWS_DEFAULT_REGION")
    queue_name = os.getenv("QUEUE_NAME")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_access_token,
        region_name=aws_region_name
    )
    
    sqs = session.resource('sqs')
    queue = sqs.get_queue_by_name(QueueName=queue_name)

    message = {
        "application": "python",
        "version": "1.0.0",
        "dependences": ["boto3", "dotent", "os", "json"]
    }

    send_message(queue, json.dumps(message))