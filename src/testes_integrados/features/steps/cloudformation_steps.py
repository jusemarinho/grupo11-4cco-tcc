from behave import given, when, then
import boto3
from dotenv import load_dotenv
import os

load_dotenv()

@given("Sou um desenvolvedor e configuro todos os tokens de acesso da AWS")
def step_impl(context):
    context.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    context.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    context.aws_access_token = os.getenv('AWS_ACCESS_TOKEN')
    context.aws_default_region = os.getenv('AWS_DEFAULT_REGION')

@given('Desejo testar meu arquivo CloudFormation passando o caminho {caminho} e o nome da stack {nome_stack}')
def step_impl(context, caminho, nome_stack):
    session = boto3.Session(aws_access_key_id = context.aws_access_key_id, aws_secret_access_key = context.aws_secret_access_key, region_name = context.aws_default_region, aws_session_token=context.aws_access_token)
    context.client = session.client('cloudformation')
    context.stack_name = nome_stack
    context.template = caminho

@given('Passo a senha do jupyter {password_jupyter} e o nome do key pair {name_key_pair}')
def step_implt(context, password_jupyter, name_key_pair):
    context.password_jupyter = password_jupyter
    context.name_key_pair = name_key_pair
    

@when("Execute a simulação de alterações de stack")
def step_impl(context):
    tags = [
        {
            'Key': 'Owner',
            'Value': 'Testes integrados'
        },
        {
            'Key': 'Environment',
            'Value': 'Development'
        }
    ]

    parameters = [
    {
        'ParameterKey': 'Ec2JupyterPassword',
        'ParameterValue': context.password_jupyter
    },
    {
        'ParameterKey': 'Ec2KeyPairName',
        'ParameterValue': context.name_key_pair
    }
]

    context.response = context.client.create_change_set(
        StackName = context.stack_name,
        TemplateBody = open(context.template).read(),
        ChangeSetName = 'test-cloudformation',
        ChangeSetType = 'CREATE',
        Description = 'Simulação de um arquivo cloud formation válido',
        Capabilities = [
            'CAPABILITY_NAMED_IAM',
        ],
        Tags = tags,
        Parameters = parameters,
        IncludeNestedStacks = False
    )

    context.stack_id = context.response['StackId']

@then("A stack devera ser criada com sucesso")
def step_implt(context):
    stack_status = None

    while stack_status != 'CREATE_COMPLETE':
        stack = context.client.describe_stacks(StackName=context.stack_name)
        stack_status = stack['Stacks'][0]['StackStatus']

    assert stack_status == 'CREATE_COMPLETE'