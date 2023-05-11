import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table_name = os.environ['TABLE_NAME']
    data = json.loads(event["body"])
    table = dynamodb.Table(table_name)
    data.update({"id": event['pathParameters']['id']})
    table.put_item(Item = data)

    # TODO implement
    return {
        'statusCode': 200,
        'body': 'successfully upload!',
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method,X-Access-Token, XKey, Authorization",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE,OPTIONS"
        }
    }
