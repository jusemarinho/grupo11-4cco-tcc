import pymongo
from urllib.parse import quote_plus
from dotenv import load_dotenv
import os

load_dotenv()

class ClientMongoDb:

    def update_result_recognator(self, endToEnd: str, result: list):
        username = quote_plus(os.getenv("MONGODB_USERNAME"))
        password = quote_plus(os.getenv("MONGODB_PASSWORD"))

        client = pymongo.MongoClient(f"mongodb://{username}:{password}@localhost:27017/ACHEI_O_BICHO")

        db = client["ACHEI_O_BICHO"]
        colecao = db["RECOGNIZE_PET"]

        endToEnd_procurado = endToEnd

        novo_resultRecognator = result

        filtro = {"endToEnd": endToEnd_procurado}
        atualizacao = {"$set": {"resultRecognator": novo_resultRecognator}}

        colecao.update_one(filtro, atualizacao)

        client.close()
