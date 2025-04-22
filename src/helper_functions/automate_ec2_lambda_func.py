import boto3
import time
import json
REGION = "us-east-2"
lambda_client = boto3.client("lambda", region_name=REGION)

def start_ec2_via_lambda() -> str:
    response = lambda_client.invoke(
        FunctionName="automate_auto_start_for_ec2_proxy_for_redis",
        InvocationType="RequestResponse",
        Payload=json.dumps({})  # if your Lambda expects input, add it here
    )

    payload = json.loads(response['Payload'].read())

    # Expecting your Lambda to return {'ip': 'x.x.x.x'} format
    try:
        ip_address = payload.get('ip')
    except Exception as e:
        raise Exception("IP address not returned by Lambda.")
    if not ip_address:
        raise Exception("IP address not returned by Lambda.")
    return ip_address

def stop_ec2_via_lambda() -> None:
    response = lambda_client.invoke(
        FunctionName="automate_auto_stop_for_ec2_proxy_for_redis",
        InvocationType="RequestResponse",
        Payload=json.dumps({})  # if your Lambda expects input, add it here
    )

    payload = json.loads(response['Payload'].read())

    # Expecting your Lambda to return {'status': 'stopped'} format
    try:
        status = payload.get('status')
    except Exception as e:
        raise Exception("Status not returned by Lambda.")
    if status != 'stopped':
        raise Exception("EC2 instance not stopped successfully.")