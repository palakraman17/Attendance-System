import boto3
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr
import cv2
import numpy as np

client=boto3.client('rekognition', region_name='us-west-2')
s3 = boto3.client('s3', region_name='us-west-2')
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
collection_id = 'ProjectCollection'
bucket = 'project-back-end-uswest2'

# Create a collection
def create_collection():
    response = client.create_collection(
        CollectionId=collection_id
    )
    print(response)

# Delete a collection
def delete_collection():
    response = client.delete_collection(
        CollectionId=collection_id
    )

# Add faces to a collection
def add_faces_to_collection(bucket,photo,collection_id):
    
    client=boto3.client('rekognition')
    response=client.index_faces(CollectionId=collection_id,
                                Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                ExternalImageId=photo,
                                MaxFaces=1,
                                QualityFilter="AUTO",
                                DetectionAttributes=['ALL'])

    print ('Results for ' + photo)  
    print('Faces indexed:')                     
    for faceRecord in response['FaceRecords']:
         print('  Face ID: ' + faceRecord['Face']['FaceId'])
         print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

    print('Faces not indexed:')
    for unindexedFace in response['UnindexedFaces']:
        print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
        print(' Reasons:')
        for reason in unindexedFace['Reasons']:
            print('   ' + reason)
    return len(response['FaceRecords'])

# Delete faces from a collection
def delete_faces(collection_id, face_ids):
    #Delete a face from collection
    print('Deleting faces from collection:' + collection_id)
    
    response = client.delete_faces(
        CollectionId=collection_id,
        FaceIds=face_ids
    )
    print(str(len(response['DeletedFaces'])) + ' faces deleted:')

# List faces in a collection
def list_faces():
    response = client.list_faces(
        CollectionId=collection_id,
        MaxResults=20,
    )

    print(response)

# Search for faces in a collection
def search_faces_by_image():
    
    with open('/tmp/image_file.jpeg', 'rb') as image:
        rekognition_response = client.search_faces_by_image(
            Image={'Bytes': image.read()},
            CollectionId=collection_id)
    
    for match in rekognition_response['FaceMatches']:
        if match['Similarity'] >= 90:
            externalImageId = match['Face']['ExternalImageId']
            netid = externalImageId.split(".")[0]
            mark_recognized_faces_present(netid)

    print("------------------Rekognition Response goes below---------------------")
    print(rekognition_response)
    #mark_unrecognized_faces_absent()
def detect_faces(bucket,photo):
   
    response = client.detect_faces(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': photo
            }
        },
        Attributes=[
            'ALL'
        ]
    )
    return response['FaceDetails']

def mark_unrecognized_faces_absent():

    table_attendance = dynamodb.Table('project_attendance')
    table_student = dynamodb.Table('Student_table')
    
    presentids_list = []
    
    if table_attendance.scan():
        pData = table_attendance.scan(FilterExpression=Attr('attendance_status').eq('Present'))

        if pData:
            for items in pData['Items']:
                presentids_list.append(items['netid'])

            print("------------------Present ids list goes below-------------------")
            print(presentids_list)
            
            sData = table_student.scan()
            
            for items in sData['Items']:
                if items['netid'] not in presentids_list:
                    now = datetime.now()
                    table_attendance.put_item(
                        Item={
                            'netid': items['netid'],
                            'attendance_status': 'Absent',
                            'approval_status':"Pending",
                            'date_time': now.strftime("%d/%m/%Y")
                        }
                    )

def mark_recognized_faces_present(netid):

    #DynamoDB connection
    table_attendance = dynamodb.Table('project_attendance')
    table_student = dynamodb.Table('Student_table')

    #Mark netid as present
    if table_attendance.scan():
        responseData = table_attendance.query(KeyConditionExpression=Key('netid').eq(netid))
        if (responseData and len(responseData['Items']) >= 1 and responseData['Items'][0]):
            pass
        else:
            now = datetime.now()
            table_attendance.put_item(
                Item={
                    'netid': netid,
                    'attendance_status': 'Present',
                    'approval_status':"Pending",
                    'date_time': now.strftime("%d/%m/%Y")
                }
            )
    else:
        now = datetime.now()
        table_attendance.put_item(
                Item={
                    'netid': netid,
                    'attendance_status': 'Present',
                    'approval_status':"Pending",
                    'date_time': now.strftime("%d/%m/%Y")
                }
            )

#if __name__ == "__main__":
def lambda_handler(event, context):
    #delete_collection()
    #create_collection()
    #add_faces_to_collection(bucket,'ss12281.png',collection_id)
    #add_faces_to_collection(bucket,'yd1405.png',collection_id)
    #add_faces_to_collection(bucket,'prp313.jpeg',collection_id)
    #add_faces_to_collection(bucket,'sl6813.jpeg',collection_id)
    #print(event)
    #list_faces()

    for key in event.get('Records'):
        file_name = key['s3']['object']['key']
        s3.download_file('project-back-end-uswest2', file_name, '/tmp/image_file.jpeg')
        FaceDetails = detect_faces(bucket,file_name)

        frame = cv2.imread('/tmp/image_file.jpeg')
        height = frame.shape[0]
        width = frame.shape[1]

        for faceDetail in FaceDetails:
            box = faceDetail['BoundingBox']
            x = int(width * box['Left'])
            y = int(height * box['Top'])
            w = int(width * box['Width'])
            h = int(height * box['Height'])

            crop_img = frame[y - 50:y + h + 50, x - 50:x + w + 50]
            cv2.imwrite('/tmp/cropped_img.jpeg', crop_img)

            with open('/tmp/cropped_img.jpeg', 'rb') as image:
                rekognition_response =client.search_faces_by_image(Image={'Bytes': image.read()}, CollectionId=collection_id)
    
                for match in rekognition_response['FaceMatches']:
                    if match['Similarity'] >= 90:
                        externalImageId = match['Face']['ExternalImageId']
                        netid = externalImageId.split(".")[0]
                        mark_recognized_faces_present(netid)

                print("------------------Rekognition Response goes below---------------------")
                print(rekognition_response)
        #search_faces_by_image()
