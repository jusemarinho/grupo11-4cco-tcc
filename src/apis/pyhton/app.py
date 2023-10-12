from recognator import Recognator
from dotenv import load_dotenv
import boto3
import os
import logging
import schedule
import time
from json import loads
from client_mongodb import ClientMongoDb

load_dotenv()

def receive_message(queue):
    try:
        messages = queue.receive_messages(MaxNumberOfMessages=10)
        if len(messages) <= 0:
            print("Not messages to receive")
            return

        for message in messages:
            message_body = loads(message.body)

            key_image = message_body["Records"][0]["s3"]["object"]["key"]

            endToEnd = key_image.split("/")[1]

            message.delete()

            if 'recognator' in key_image:
                recognator = Recognator()
                prediction = recognator.predict(file_key=key_image)
                client_mongodb = ClientMongoDb()
                client_mongodb.update_result_recognator(endToEnd, prediction)
                return prediction
            
    except Exception as error:
        logging.exception("Receive message failed.")
        raise error

def main():
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

    schedule.every(5).seconds.do(receive_message, queue)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
