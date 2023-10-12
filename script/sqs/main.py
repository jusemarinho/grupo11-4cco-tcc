import boto3
from dotenv import load_dotenv
import os
from json import loads
import logging
import schedule
import pymongo
import time

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

            print(message_body)

            update_result_recognator(endToEnd, 'Golden')

            message.delete()
    except Exception as error:
        logging.exception("Receive message failed.")
        raise error
    

def update_result_recognator(endToEnd: str, result: str):
    client = pymongo.MongoClient("mongodb://localhost:27017")  

    db = client["ACHEI_O_BICHO"]
    colecao = db["RECOGNIZE_PET"]

    endToEnd_procurado = endToEnd

    novo_resultRecognator = result

    filtro = {"endToEnd": endToEnd_procurado}
    atualizacao = {"$set": {"resultRecognator": novo_resultRecognator}}

    colecao.update_one(filtro, atualizacao)

    client.close()

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

    schedule.every(2).seconds.do(receive_message, queue)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()