import json
import boto3.dynamodb
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_perm = dynamodb.Table('permanent-attendance')
table_attendance=dynamodb.Table('project_attendance')
def lambda_handler(event, context):
    # TODO implement
    
    
    #print(event)
    responseData = table_perm.scan()
    print(responseData)
    
    i=responseData['Count']
    
    for ite in event['Items']:
        i=i+1
        table_perm.put_item(
		Item={
				'number': i,
				'netid':ite['netid'],
				'attendance_status': ite['attendance'],
				'date_time': ite['date']
		}
        )
    
    
    responseData2= table_attendance.scan()
    
    for ite in responseData2['Items']:
        #print(item)
        
        i=i+1
        table_perm.put_item(
		Item={
				'number': i,
				'netid':ite['netid'],
				'attendance_status': ite['attendance_status'],
				'date_time': ite['date_time']
		}
        )
        
        print(ite['netid'])
        table_attendance.delete_item(
        Key={
        'netid': ite['netid'],
        'date_time':ite['date_time']
        }
        )
        
    print(responseData2)
        
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
