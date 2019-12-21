import json
import boto3.dynamodb
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table_attendance = dynamodb.Table('project_attendance')
table_student = dynamodb.Table('Student_table')

""" def fetch():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table_passcodes = dynamodb.Table('project_attendance')
    responseData = table_passcodes.scan(
        FilterExpression=Attr("approval_status").eq('Pending') & Attr("attendance_status").eq('Present')
    )
    return responseData """

def getabsentees():
    presentids_list , absentids_list = [],[]
    date='01/01/1996'
    day_present={'date_time':"",'netids':[]}
    dictionary={'Items':[]}
    pData = table_attendance.scan()
    #print(pData)
    
    for items in pData['Items']:
        if  items['date_time']==date:
            #print('in if')
            presentids_list.append(items['netid'])
        else:
            #print('in else')
            if date!='01/01/1996':
                day_present['date_time']=date
                day_present['netids']=presentids_list
                dictionary['Items'].append(day_present)
            date=items['date_time']
            #day_present['date_time']=date
            presentids_list=[]
            presentids_list.append(items['netid'])
            day_present={'date_time':'','netids':[]}
            
        
    day_present['netids']=presentids_list
    day_present['date_time']=items['date_time']
    dictionary['Items'].append(day_present)

    print(dictionary)
    absentids_list=[]
    absent={'date_time':'', 'netid':''}
    response={'Items':[]}
    
    sData = table_student.scan()
    for clas in dictionary['Items']:
        date=clas['date_time']
        for items in sData['Items']:
            if items['netid'] not in clas['netids']:
                absent['date_time']=date
                absent['netid']=items['netid']
                absentids_list.append(absent)
                absent={'date_time':'', 'netid':''}
    response['Items']=absentids_list
    print(response)
    return response 

def lambda_handler(event, context):
    '''
    response={}
    
    presentids_list , absentids_list = [],[]
    
    pData = table_attendance.scan()
    
    for items in pData['Items']:
        presentids_list.append(items['netid'])
    
    print("presen ids go here")    
    print(presentids_list)
    
    sData = table_student.scan()
    
    for items in sData['Items']:
        if items['netid'] not in presentids_list:
            absentids_list.append(items['netid'])
            
    print("absent ids go here")      
    print(absentids_list)
    '''
    '''
    for item in absentids_list:
        responseData = table_attendance.query(KeyConditionExpression=Key('netid').eq(netid))
		if (responseData and len(responseData['Items']) >= 1 and responseData['Items'][0]):
	'''
    '''
    response['Items'] = absentids_list
    
'''
    return {
        "statusCode": 200,
        "body": json.dumps(getabsentees())
    }

    
