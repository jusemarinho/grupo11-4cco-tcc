import functions_framework
import json
import logging

@functions_framework.http
def hello_http(request):    
    try:
        request_args = request.get_json()

        if not request_args:
            return {"error": "A solicitação não contém um corpo."}

        response_json = json.dumps(request_args)

        return response_json, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        logging.exception(e)
        raise
