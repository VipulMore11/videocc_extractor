from celery import shared_task
import boto3
import subprocess
import os
from django.conf import settings

@shared_task
def process_video(video_name, upload_uuid):
    ccextractor_path = '/home/ubuntu/videocc_extractor/run_ccextractor.sh'
    
    video_path = os.path.join('/home/ubuntu/downloads', video_name)
    print(video_path)
    srt_path = os.path.splitext(video_path)[0] + '.srt'
    print(srt_path)
    try:
        s3 = boto3.client('s3',
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          region_name=settings.AWS_S3_REGION_NAME)
        dynamodb = boto3.resource('dynamodb',
                                  aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                  region_name=settings.AWS_S3_REGION_NAME)
        print("Download started")
        s3.download_file(settings.AWS_STORAGE_BUCKET_NAME, video_name, video_path)
        print(f"Downloaded video to {video_path}")
        
        subprocess.run(
            [ccextractor_path, video_path, '-o', srt_path],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Subtitles extracted to {srt_path}")
        
        with open(srt_path, 'r', encoding='utf-8') as f:
            subtitles = f.read().strip().split('\n\n')
        
        table = dynamodb.Table(settings.DYNAMO_TABLE_NAME)
        
        for subtitle in subtitles:
            parts = subtitle.split('\n')
            if len(parts) >= 3:
                timestamp = parts[1].split(' --> ')[0]
                subtitle_text = ' '.join(parts[2:])
                table.put_item(Item={
                    'uuid': upload_uuid,
                    'video_name': video_name,
                    'timestamp': timestamp,
                    'subtitle_text': subtitle_text
                })
        
        print("Subtitles stored in DynamoDB")
    except subprocess.CalledProcessError as e:
        print(f"Error extracting subtitles: {e}")
        print(f"Subprocess output: {e.stdout.decode()}")
        print(f"Subprocess error output: {e.stderr.decode()}")
    except boto3.exceptions.Boto3Error as e:
        print(f"AWS error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if os.path.exists(video_path):
            os.remove(video_path)
            print(f"Removed temporary video file {video_path}")
        if os.path.exists(srt_path):
            os.remove(srt_path)
            print(f"Removed temporary subtitle file {srt_path}")