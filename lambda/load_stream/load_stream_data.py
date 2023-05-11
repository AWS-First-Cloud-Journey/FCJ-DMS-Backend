import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
import os

region = 'ap-southeast-1' # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

host = os.getenv("SEARCH_DOMAIN") # The OpenSearch domain endpoint with https:// and without a trailing slash
index = 'doc'
datatype = '_doc'
url = "https://" + host + '/' + index + '/' + datatype + '/'

# Lambda execution starts here
def lambda_handler(event, context):
    count = 0
    headers = { "Content-Type": "application/json" }
    for record in event['Records']:
        # Get the primary key for use as the OpenSearch ID
        print(record['dynamodb']['Keys'])
        id = record['dynamodb']['Keys']['user_id']['S']
        file_name = record['dynamodb']['Keys']['file']['S']
        
        if record['eventName'] == 'REMOVE':
            r = requests.delete(url + id + file_name, auth=awsauth)
        else:
            document = record['dynamodb']['NewImage']
            r = requests.put(url + id + file_name, auth=awsauth, json=document, headers=headers)
        count += 1
    print("count", count)
    return str(count) + ' records processed.'