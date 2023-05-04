# Como criar uma política de acesso para uma fila do Amazon SQS

Aqui estão os passos para criar uma política de acesso para uma fila do Amazon SQS usando a console da AWS, este tutorial parte do pressuposto que você já tem o recurso do SQS criado:

<h2>Passo 1: Crie uma política de acesso para a sua fila</h2>

1 - Acesse a console do Amazon SQS e selecione a fila que você criou.

2 - Clique na guia "Permissões" e em seguida, clique em "Adicionar política de fila".

3 - Na página "Adicionar política de fila", selecione o serviço ou usuário que você deseja conceder acesso à fila.

4 - Escolha as ações permitidas e especifique as condições, se necessário. Por exemplo, para permitir que o S3 envie mensagens para a fila, você precisará definir a condição ArnLike para corresponder ao ARN do bucket do S3 que enviará as mensagens.

5 - Cole a política de acesso diretamente na área de texto ou crie uma nova política usando o assistente. Aqui está um exemplo de política que permite que o S3 envie mensagens para a fila:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "s3.amazonaws.com"
      },
      "Action": "sqs:SendMessage",
      "Resource": "arn:aws:sqs:REGION:ACCOUNT-ID:QUEUE-NAME",
      "Condition": {
        "ArnLike": {
          "aws:SourceArn": "arn:aws:s3:::BUCKET-NAME"
        }
      }
    }
  ]
}
```
6 - Lembre-se de substituir <b>'REGION'</b>, <b>'ACCOUNT-ID'</b>, <b>'QUEUE-NAME'</b> e <b>'BUCKET-NAME'</b> pelos valores reais correspondentes às suas configurações.

6.1 - Para obter essas informações entre no console da aws (AWS CLI) e digite:
```sh
aws sts get-caller-identity
```
```
aws configure get region
```

7 - Quando terminar, clique em "Salvar alterações" para aplicar a política à fila do SQS.

<h2>Passo 2: Obtenha as credenciais de acesso para a sua aplicação</h2>

1 - Acesse a console do IAM e crie um usuário para sua aplicação.

2 - Conceda as permissões necessárias para o usuário acessar a fila do SQS.

3 - Obtenha as credenciais de acesso para o usuário criado.

<h2>Passo 3: Use as credenciais para enviar mensagens para a fila do SQS</h2>

1 - Use as credenciais de acesso para autenticar sua aplicação e enviar mensagens para a fila do SQS.

<br>
<br>

# Configurar Notificações de Eventos no S3 para enviar ao SQS

<b>Esta parte do tutorial assume que você já tem seu recurso do S3 criado.</b>

1 - Navegue até o S3, selecione seu bucket.

2 - Vá em propriedades e procure pelo tópico <b>Notificações de eventos </b>

3 - Clique em <b>*Criar Notificação de evento*</b>. Preencha algumas infomações como:

- Nome do evento
- Prefiro - Opcional (se não houver ele vai verificar todos os diretórios)
- Sufixo - Opcional (se nçao houver ele vai verificar todos os tipos de arquivos)


4 - Tipos de Eventos <br>
<code>Aqui você coloca o que preferir</code>

5 -  Por fim, selecione o Destino, escolha <b>'Fila do SQS'</b>

- Escolher entre seus filas do SQS

E escolha sua fila. No final salve.

6 - Agora teste, assim que você inserir um arquivo deverá receber uma mensagem como essa no SQS:

```json
{
  "Records": [
    {
      "eventVersion": "2.1",
      "eventSource": "aws:s3",
      "awsRegion": "us-east-1",
      "eventTime": "2023-05-04T02:27:25.626Z",
      "eventName": "ObjectCreated:Put",
      "userIdentity": {
        "principalId": "AWS:XXXXXXXXXXXXXXXXXXX:userXXXXXXXXXXXX"
      },
      "requestParameters": {
        "sourceIPAddress": "XXX.XXX.XXX.XXX"
      },
      "responseElements": {
        "x-amz-request-id": "XXXXXXXXXXXXXX",
        "x-amz-id-2": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
      },
      "s3": {
        "s3SchemaVersion": "1.0",
        "configurationId": "sqs-trigger",
        "bucket": {
          "name": "example-bucket",
          "ownerIdentity": {
            "principalId": "XXXXXXXXXXXX"
          },
          "arn": "arn:aws:s3:::example-bucket"
        },
        "object": {
          "key": "example/file.txt",
          "size": 1234,
          "eTag": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
          "sequencer": "XXXXXXXXXXXXXXXXXX"
        }
      }
    }
  ]
}

```

Você pode ver melhor aqui: https://docs.aws.amazon.com/pt_br/AmazonS3/latest/userguide/ways-to-add-notification-config-to-bucket.html#S3NotificationHowToDestinationSQS

