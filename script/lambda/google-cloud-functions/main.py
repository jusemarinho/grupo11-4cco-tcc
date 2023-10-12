import functions_framework
import numpy as np
import os
from google.cloud.exceptions import NotFound
import boto3
import botocore.exceptions
import os
import cv2
import base64


@functions_framework.http
def save_image_pet(request):
    request_json = request.get_json()

    path = request_json.get("fileName")
    buffer_base64 = request_json.get("buffer")
    mimetype = request_json.get("contentType")

    location = upload_image_s3(path, mimetype, buffer_base64)
    return {"message": "Image uploaded successfully", "location": location}

def upload_image_s3(path: str, content_type: str, buffer_string):
    try:
        s3 = client_s3()
        bucket_name = "pilha-nuvem-tcc-sptech-bucket"
        
        print("Saving File in AWS...")
        print(bucket_name, content_type)
        s3.put_object(Bucket=bucket_name, Key=path, ContentType=content_type, Body=buffer_string)

        location = f"s3://{bucket_name}/{path}"
        return location
    except botocore.exceptions.NoCredentialsError:
        print('AWS credentials not found. Make sure you have AWS credentials configured.')
    except Exception as e:
        print(f'Error uploading file to S3: {str(e)}')

def client_s3() -> boto3.Session:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_access_token = os.environ.get("AWS_ACCESS_TOKEN")
    aws_region_name = os.environ.get("AWS_DEFAULT_REGION")

    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_access_token,
        region_name=aws_region_name
    )

    return session.client('s3')
  
def create_opencv_image_from_stringio(img_stream, cv2_img_flag=0):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)

def create_buffer_string_from_imagecv2(img):
    cap = cv2.VideoCapture(0)
    retval, image = cap.read()
    retval, buffer = cv2.imencode('.jpg', image)
    jpg_as_text = base64.b64encode(buffer)
    return jpg_as_text

def resize_photo(img):
    imagem = cv2.imread('/home/patrick/SPTECH/TCC/img-test-tcc/teste4.jpg')
    largura_fixa = 800
    proporcao = largura_fixa / imagem.shape[1]
    altura_fixa = int(imagem.shape[0] * proporcao)
    imagem_redimensionada = cv2.resize(imagem, (largura_fixa, altura_fixa))

    imagem_em_escala_de_cinza = cv2.cvtColor(imagem_redimensionada, cv2.COLOR_BGR2GRAY)
    imagem_equalizada = cv2.equalizeHist(imagem_em_escala_de_cinza)

    imagem_suavizada = cv2.GaussianBlur(imagem_equalizada, (5, 5), 0)
    classificador_gatos = cv2.CascadeClassifier('/home/patrick/SPTECH/TCC/img-test-tcc/haarcascade_frontalcatface_extended.xml')

    classificador_cachorros = cv2.CascadeClassifier('/home/patrick/SPTECH/TCC/img-test-tcc/haarcascade_frontalface_alt2.xml')

    gatos = classificador_gatos.detectMultiScale(
    imagem_em_escala_de_cinza,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30)
    )

    cachorros = classificador_cachorros.detectMultiScale(
    imagem_em_escala_de_cinza,
    scaleFactor=1.9,
    minNeighbors=1,
    )

    def area_retangulo(retangulo):
        x, y, w, h = retangulo
        return w * h

    objeto_cortado = None

    if len(gatos) > 0:
        maior_area_gato = max(gatos, key=area_retangulo)
        x, y, w, h = maior_area_gato
        cv2.rectangle(imagem_redimensionada, (x, y), (x + w, y + h), (0, 255, 0), 2)
        objeto_cortado = imagem_redimensionada[y:y + h, x:x + w]

    elif len(cachorros) > 0:
        maior_area_cachorro = max(cachorros, key=area_retangulo)
        x, y, w, h = maior_area_cachorro
        cv2.rectangle(imagem_redimensionada, (x, y), (x + w, y + h), (0, 255, 0), 2)
        objeto_cortado = imagem_redimensionada[y:y + h, x:x + w]

    cv2.imwrite('imagem_com_retangulos.jpg', imagem_redimensionada)

    if objeto_cortado is not None:
        cv2.imwrite('objeto_cortado.jpg', objeto_cortado)
