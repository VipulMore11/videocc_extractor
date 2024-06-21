from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .tasks import process_video
import boto3
from django.conf import settings
from boto3.dynamodb.conditions import Attr
import uuid

def upload_video(request):
    upload_success = False
    error_message = None
    
    if request.method == 'POST':
        if 'video' not in request.FILES:
            return HttpResponseBadRequest("No video file uploaded")
        
        video = request.FILES['video']
        try:
            s3 = boto3.client('s3')
            s3.upload_fileobj(video, settings.AWS_STORAGE_BUCKET_NAME, video.name)
            
            # Generate a UUID for the upload
            upload_uuid = str(uuid.uuid4())
            
            # Store the UUID in the session
            if 'upload_uuids' not in request.session:
                request.session['upload_uuids'] = []
            request.session['upload_uuids'].append(upload_uuid)
            request.session.modified = True
            
            # Pass the UUID to the processing task
            process_video.delay(video.name, upload_uuid)
            print("Upload successful")
            upload_success = True
        except Exception as e:
            error_message = f"Error uploading video: {str(e)}"
            print(error_message)
    
    return render(request, 'upload.html', {'upload_success': upload_success, 'error_message': error_message})
    
    return render(request, 'upload.html')

def homepage(request):
    return render(request, 'home.html')

def search(request):
    items = None
    error_message = None

    if 'q' in request.GET:
        keyword = request.GET['q']
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(settings.DYNAMO_TABLE_NAME)
            
            # Get UUIDs from session
            upload_uuids = request.session.get('upload_uuids', [])
            
            if not upload_uuids:
                error_message = "No uploaded videos found in session."
                print(error_message)
            else:
                # Query DynamoDB for subtitles containing the keyword and matching the UUIDs
                filter_expression = Attr('subtitle_text').contains(keyword) & Attr('uuid').is_in(upload_uuids)
                response = table.scan(FilterExpression=filter_expression)
                
                items = response.get('Items', [])
                if not items:
                    error_message = "No results found."
                    print(error_message)
        except Exception as e:
            error_message = f"Error searching subtitles: {str(e)}"
            print(error_message)

    return render(request, 'search.html', {'items': items, 'error_message': error_message})
