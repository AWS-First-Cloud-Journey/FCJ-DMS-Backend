import boto3
import json
import requests
from requests_aws4auth import AWS4Auth
import os

region = 'ap-southeast-1'  # For example, us-west-1
service = 'es'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key,
                   region, service, session_token=credentials.token)

# The OpenSearch domain endpoint with https:// and without a trailing slash
host = os.getenv("SEARCH_DOMAIN")
index = 'doc'
url = "https://" + host + '/' + index  + '/_search'

# Lambda execution starts here


def lambda_handler(event, context):
    # Put the user query into the query DSL for more accurate search results.
    # Note that certain fields are boosted (^).
    #field = "{}.S".format(event['queryStringParameters']['field'])
    query = {
        "size": 25,
        "query": {
            "bool": {
                "must": [
                    {
                      "match": {
                            "user_id.S":  event['pathParameters']['id']
                        }
                    },
                    {
                        "bool": {
                            "should": [
                                {
                                    "match": {
                                        event['queryStringParameters']['field']: event['queryStringParameters']['key']
                                    }
                                }
                            ]
                        }
                    }
                ]
            }
        }
    }

    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = {"Content-Type": "application/json"}

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers,
                         data=json.dumps(query))
    
    print(r.text)
    # Create the response and add some extra content to support CORS
    response = {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": '*'
            },
            "isBase64Encoded": False
    }
    response['body'] = r.text    
    return response