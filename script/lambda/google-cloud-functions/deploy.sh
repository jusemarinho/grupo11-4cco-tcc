PROJECT_ID=projetct-lambda-tcc
FUNCTION_NAME=function-test
REGION=us-central1
RUNTIME=python311
ENTRY_POINT=hello_http

# Faz o deploy da função
gcloud functions deploy $FUNCTION_NAME \
    --project=$PROJECT_ID \
    --region=$REGION \
    --runtime=$RUNTIME \
    --entry-point=$ENTRY_POINT \
    --trigger-http \
    --allow-unauthenticated \
    --memory=256MB \
    --source=.
