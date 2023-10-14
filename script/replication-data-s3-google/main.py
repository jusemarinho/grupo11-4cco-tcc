import boto3
import os
from dotenv import load_dotenv
import logging

logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

def main():
    aws_access_key_id = os.getenv("aws_access_key_id")
    aws_secret_access_key = os.getenv("aws_secret_access_key")
    aws_access_token = os.getenv("aws_session_token")
    aws_region_name = os.getenv("aws_default_region")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_access_token,
        region_name=aws_region_name
    )

    origem_bucket_name = 'pilha-nuvem-tcc-sptech-bucket'
    destino_bucket_name = 'pilha-nuvem-tcc-sptech-bucket-replication'

    s3 = session.client(service_name='s3')

    objects = s3.list_objects(Bucket=origem_bucket_name)

    s3.create_bucket(Bucket=destino_bucket_name)

    for obj in objects.get('Contents', []):
        key = obj['Key']
        s3.copy_object(CopySource={'Bucket': origem_bucket_name, 'Key': key},
                    Bucket=destino_bucket_name,
                    Key=key)
        logger.info(f"Copiado: {key}")

    logger.info("Concluído!")

if __name__ == "__main__":
    main()
