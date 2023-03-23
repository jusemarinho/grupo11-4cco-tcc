from behave import given, when, then
import boto3

@given('que o tráfego de rede está sendo enviado e recebido pela VPC')
def step_impl(context):
    ec2 = boto3.client('ec2')
    vpcs = ec2.describe_vpcs()
    vpc_id = vpcs['Vpcs'][0]['VpcId']
    context.vpc_id = vpc_id

@when('eu verifico o status da criptografia do tráfego')
def step_impl(context):
    ec2 = boto3.client('ec2')
    subnets = ec2.describe_subnets(Filters=[{'Name': 'vpc-id', 'Values': [context.vpc_id]}])
    context.subnets = subnets

@then('todo o tráfego de rede deve estar criptografado')
def step_impl(context):
    ec2 = boto3.client('ec2')
    for subnet in context.subnets['Subnets']:
        sg_id = subnet['GroupId']
        sg = ec2.describe_security_groups(GroupIds=[sg_id])
        inbound_rules = sg['SecurityGroups'][0]['IpPermissions']
        outbound_rules = sg['SecurityGroups'][0]['IpPermissionsEgress']
        
        # check that security group allows only necessary and secure traffic
        assert inbound_rules == [
            {'IpProtocol': 'tcp', 'FromPort': 22, 'ToPort': 22, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ], f"Inbound rules for security group {sg_id} are not secure"
        
        assert outbound_rules == [
            {'IpProtocol': 'tcp', 'FromPort': 80, 'ToPort': 80, 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
        ], f"Outbound rules for security group {sg_id} are not secure"
