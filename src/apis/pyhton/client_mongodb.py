import pymongo

class ClientMongoDb:

    def update_result_recognator(self, endToEnd: str, result: str):
        client = pymongo.MongoClient("mongodb://localhost:27017")  

        db = client["ACHEI_O_BICHO"]
        colecao = db["RECOGNIZE_PET"]

        endToEnd_procurado = endToEnd

        novo_resultRecognator = result

        filtro = {"endToEnd": endToEnd_procurado}
        atualizacao = {"$set": {"resultRecognator": novo_resultRecognator}}

        colecao.update_one(filtro, atualizacao)

        client.close()
