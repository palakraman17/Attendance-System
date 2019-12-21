import json
import boto3.dynamodb

def fetch():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table_passcodes = dynamodb.Table('Student_table')
    responseData = table_passcodes.scan()
    print(responseData)
    return responseData

def lambda_handler(event, context):

    return {
        'statusCode': 200,
        'body': fetch()
    }
