import functions_framework

@functions_framework.http
def hello_http(request):    
    request_json = request.get_json(silent=True)
    request_args = request.args

    return '{}'.format(request_json)