import boto3
import json
from dotenv import load_dotenv
import os
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import cv2
import numpy as np

load_dotenv()


class FindImage:
    def __init__(
        self, flag: bool = None, bucket_name: str = None, resource_name: str = None
    ) -> None:
        self.flag = flag
        if self.flag:
            self.session = self.create_session_boto3()
            self.bucket_name = bucket_name
            self.resource = self.create_resource(resource_name, self.session)
            self.s3_bucket = self.s3(bucket_name, self.resource)
            self.client = self.create_client_boto3()

    def create_session_boto3(self):
        session = boto3.Session(
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )

        return session

    def create_client_boto3(self): 
        client = boto3.client(
            's3', 
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            aws_session_token=os.getenv("AWS_SESSION_TOKEN"),
            region_name=os.getenv("AWS_DEFAULT_REGION"),
        )

        return client

    def download_images_training(self, local_path: str, prefix: str):
        objects = self.client.list_objects_v2(Bucket=os.getenv("BUCKET_S3"), Prefix=prefix)

        for obj in objects.get('Contents', []):
            key = obj['Key']
            if obj['Size'] > 0:  # Ignorar pastas vazias
                local_file_path = os.path.join(local_path, key[len(prefix):])
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
                self.client.download_file(os.getenv("BUCKET_S3"), key, local_file_path)
                print(f'Arquivo baixado: {local_file_path}')
    
        for obj in objects.get('CommonPrefixes', []):
            subfolder_key = obj['Prefix']
            subfolder_path = os.path.join(local_path, subfolder_key[len(prefix):])
            self.download_images_training(subfolder_key, subfolder_path)

    def create_resource(self, resource: str, session: boto3.Session):
        return session.resource(resource)

    def s3(self, bucket_name, resource: str):
        return resource.Bucket(bucket_name)
    
    def download(self, file_key: str, path_download: str):
        file_object = self.s3_bucket.Object(os.getenv('BUCKET_S3'), file_key)
        file_object.download_file(path_download)

    def find(
        self, md5: str, user_id: str = None, id_pet: str = None, name_pet: str = None
    ):
        if self.flag:
            image_key = f"train/{user_id}/{id_pet}/{name_pet}_{md5}.jpg"
            print(image_key)
            obj = self.s3_bucket.Object(image_key)
            image_data = obj.get()["Body"].read()
            image = Image.open(BytesIO(image_data))
            image_array = np.array(image)
            image = cv2.imread(image_array)
        else:
            # procurar fotos localmente
            local_image_path = f"./train/{md5}.jpg"
            if os.path.exists(local_image_path):
                image = cv2.imread(local_image_path)
            else:
                print("A imagem não foi encontrada localmente.")
                return

        return image
    
    



if __name__ == "__main__":
    find_image = FindImage(flag=False)
    find_image.find("50fcbd042ae9a24e3afd5cbb8e1e4542")
