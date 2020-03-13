import json
import urllib.parse
import boto3
import email
import string
import os
import io

print('Loading function')

s3 = boto3.client('s3')
s3r = boto3.resource('s3')
outputBucket = "zefix-email-attachments"

pdfDir = "/tmp/output/"



def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])

        msg = email.message_from_string(response.get("Body").read().decode('utf-8'))
        
        print(len(msg.get_payload()))
        
        if len(msg.get_payload()) == 2:

            # Create directory for XML files (makes debugging easier)
            if os.path.isdir(pdfDir) == False:
                os.mkdir(pdfDir)

            # The first attachment
            attachment = msg.get_payload()[1]
            
            print(attachment.get_content_type())


        else:
            print("Could not see file/attachment.")
        
        return 0
        
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
