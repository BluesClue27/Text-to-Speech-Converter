import json
import boto3
import uuid
import os
from datetime import datetime

# Initialize AWS clients
polly_client = boto3.client('polly')
s3_client = boto3.client('s3')
BUCKET_NAME = os.environ['S3_BUCKET_NAME']
   
def lambda_handler(event, context):
    try:
        # Log the event to inspect its structure
        print("Received event:", event)
        body = json.loads(event['body'])
        text = body.get('text','') 
        voice_id = body.get('voiceId', 'Joanna')  # Default to 'Joanna' if 'voiceId' is missing
        
        if not text:
            return {
                'statusCode': 400,
                'headers': {
                    "Access-Control-Allow-Origin": "*",
                    "Access-Control-Allow-Headers": "Content-Type",
                    "Access-Control-Allow-Methods": "OPTIONS,POST"
                },
                'body': json.dumps({'message': 'Text is required'})
            }

        # Generate a unique file name for the MP3 file
        file_name = f"logs/{uuid.uuid4()}.mp3"
        
        # Call Polly to synthesize the speech
        response = polly_client.synthesize_speech(
            Text=text,
            VoiceId=voice_id,
            OutputFormat='mp3',
            SampleRate='22050'
        )
        
        # Read the audio stream into bytes
        audio_stream = response['AudioStream'].read()

        # Store the audio stream (MP3 data) in S3
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=file_name,
            Body=audio_stream,
            ContentType='audio/mpeg'
        )
        
        # Generate a pre-signed URL for accessing the MP3 file
        url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': file_name},
            ExpiresIn=3600  # URL expires in 1 hour
        )
        
        # Return the pre-signed URL to the web-based UI
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            'body': json.dumps({'url': url})
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            'body': json.dumps({'message': 'Internal server error'})
        }
