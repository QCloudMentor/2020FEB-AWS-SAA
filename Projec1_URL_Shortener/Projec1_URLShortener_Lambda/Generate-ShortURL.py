# Generate-ShortURL
# Evironment Variables: API_endpoint = https://xxx.cloudfront.net/api
#                      DBTableName = TableURLShortener
# Role: iamrole-lambda-put-data-to-dynamodb


import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr


def lambda_handler(event, context):
    # TODO implement

    env_DBTableName = os.environ['DBTableName']
    env_API_endpoint = os.environ['API_endpoint']

    print("env_DBTableName:" + env_DBTableName)
    
    print(event)
    OriginalURL = event["Url"]
    print("OriginalURL:"+ OriginalURL)
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(env_DBTableName)
    
    # Table Query
    Url_Item = table.query(
        KeyConditionExpression=Key("OriginalURL").eq(OriginalURL)
    )

    ShortURL = ""
    ShortURL_token = ""
    
    if len(Url_Item["Items"]) > 0:
        #exist
        ShortURL_token = Url_Item["Items"][0]["ShortURL"]
        print("ShortURL_token from DB:" , ShortURL_token)
    else:
        #New item
        print("Append new item.")

        #Use HashIds to generate hash code of OriginalURL
        import time
        import random
        from hashids import Hashids
        
        created_time_digit = time.strftime("%Y%m%d%H%M%S")
        r = random.randint(1,99999)
        random_digit = str(r).zfill(5)
        tiny_id = created_time_digit + random_digit
        pk = int(tiny_id)  # Your object's id
        hashids = Hashids(salt='My salt string', min_length=9)
        ShortURL_token = hashids.encode(pk)
        
        
        #Put new item into DynamoDB -----------------------------------------------
        dynamodb_client = boto3.client("dynamodb")
        dynamodb_client.put_item(
            TableName=env_DBTableName,
            Item={
                "OriginalURL": {"S": OriginalURL},
                "ShortURL": {"S": ShortURL_token},
                "TinyId": {"N": tiny_id},
            })
        print('Insert new Url into table')
    
    ShortURL = '{domain}/{link_id}'.format(domain=env_API_endpoint, link_id=ShortURL_token)
    print("Hi ShortURL:" + ShortURL)    
    
    return ShortURL
