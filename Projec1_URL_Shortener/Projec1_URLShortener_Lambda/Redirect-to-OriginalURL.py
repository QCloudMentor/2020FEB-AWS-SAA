# Redirect-to-OriginalURL
# Evironment Variables: URLShortenerWebsite = https://xxx.cloudfront.net/
#                       DBTableName = TableURLShortener
# Role: iamrole-lambda-put-data-to-dynamodb

import json
import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

def check_availability(element, collection: iter):
    result = element in collection
    
    item = ""
    if result == True:
        if collection[element] == "":
            item = "n/a"
        else:    
            item = collection[element]
    else: 
        item = "n/a"
        
    return item
    
    
def lambda_handler(event, context):
    # TODO implement
    
    env_DBTableName = os.environ['DBTableName']
    env_URLShortenerWebsite = os.environ['URLShortenerWebsite']
    
    print(env_DBTableName)
    print("event:" + json.dumps(event))

    #print("event:" + event.items[0])
    
    input_valided = False
    pathParameters = check_availability('pathParameters', event)
    proxy = ""
    if pathParameters != "n/a":
        ShortURL_token = check_availability('proxy', event["pathParameters"])
        if proxy != "n/a":
            input_valided = True
    
    if input_valided == False:
        return env_URLShortenerWebsite
    else:
        print("ShortURL_token:", ShortURL_token)
        
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(env_DBTableName)
        filter_expression = Key('ShortURL').eq(ShortURL_token) 
        projection_expression = '#i' 
        expression_attributeNames =  {'#i':'OriginalURL' } 
        Url_Item = table.scan(
             FilterExpression=filter_expression,
             ProjectionExpression=projection_expression,
             ExpressionAttributeNames=expression_attributeNames
        )
        
        OriginalURL = ""
        if len(Url_Item["Items"]) > 0:
            
            OriginalURL = Url_Item["Items"][0]['OriginalURL']
        else:
            return env_URLShortenerWebsite

    return {
        'statusCode': 301,
        'body': '',
        'headers' : {
                 'Location': OriginalURL
         }
    }