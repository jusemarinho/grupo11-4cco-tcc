from tensorflow.keras.preprocessing import image
import tensorflow as tf
import numpy as np
import os
from dotenv import load_dotenv
from find_image import FindImage
import botocore
import json

load_dotenv()

class Recognator:
  def __init__(self) -> None:
    self.loaded_model = tf.keras.models.load_model(os.getenv('MODEL_PATH'))
    self.class_names_generated = None
    with open(os.getenv('CLASSES_FILE_PATH'), 'r') as file:
      self.class_names_generated = json.load(file)

  def predict(self, file_key):
    
    s3 = FindImage(flag=True, bucket_name=os.getenv("BUCKET_S3"), resource_name="s3")

    try:
        print(file_key)
        path_download = os.path.join(os.getenv('PATH_DOWNLOAD_IMG'), file_key.split("/")[2])
        s3.download(file_key, path_download)
        print(f"Arquivo baixado com sucesso.")
        prediction = self.match_pet(self.loaded_model, self.class_names_generated, file_key.split("/")[2])
        return prediction
    except botocore.exceptions.NoCredentialsError:
        print("Credenciais não encontradas ou inválidas.")
    except botocore.exceptions.ClientError as e:
        if e.response["Error"]["Code"] == "404":
            print("O arquivo não foi encontrado no bucket.")
        else:
            print("Erro desconhecido ao baixar o arquivo:", e)


  def match_pet(self, model, labels, name_object):
    # Concatenando nome do objeto e diretorio local
    path_image = f'{os.getenv("PATH_DOWNLOAD_IMG")}{name_object}'

    # Carregando e redimensionando a imagem
    img = image.load_img(path_image, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalização

    # Fazendo a previsão
    prediction = model.predict(img_array)
    
    # Obtendo a classe prevista
    predicted_class_index = np.argmax(prediction)

    # Obtendo o nome da classe
    predicted_class = labels[f"{predicted_class_index}"]

    # Imprimindo a classe prevista
    print(predicted_class)
    return predicted_class