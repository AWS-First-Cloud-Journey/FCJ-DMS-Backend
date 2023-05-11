import json
import boto3
import os
from decimal import *
from boto3.dynamodb.types import TypeDeserializer

dynamodb = boto3.client('dynamodb') 
serializer = TypeDeserializer()
    
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
        
def deserialize(data):
    if isinstance(data, list):
        return [deserialize(v) for v in data]

    if isinstance(data, dict):
        try:
            return serializer.deserialize(data)
        except TypeError:
            return {k: deserialize(v) for k, v in data.items()}
    else:
        return data
        
def lambda_handler(event, context):
    # TODO implement
    table_name = os.environ['TABLE_NAME']
    user_id = event['pathParameters']['id']
    print(user_id)
    data = dynamodb.query(
        TableName=table_name,
        KeyConditionExpression="id = :id",
        ExpressionAttributeValues={ ":id": { 'S': user_id } }
    )
    
    format_data = deserialize(data["Items"])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,PUT,POST,DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Access-Control-Allow-Headers, Origin,Accept, X-Requested-With, Content-Type, Access-Control-Request-Method,X-Access-Token,XKey,Authorization"
        },
        "body": json.dumps(format_data, cls=DecimalEncoder)
        #"body": format_data
    }
