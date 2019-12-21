import json
import boto3.dynamodb
from boto3.dynamodb.conditions import Key, Attr

def fetch():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table_attendance = dynamodb.Table('permanent-attendance')
    responseData = table_attendance.scan(ProjectionExpression='date_time')
    print(responseData)
    
   
    return responseData


def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': fetch()
    }
