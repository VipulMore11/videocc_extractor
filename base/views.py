from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from .tasks import process_video
import boto3
from boto3.dynamodb.conditions import Attr
from django.conf import settings
from django.http import JsonResponse
from celery.result import AsyncResult

def check_task_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        'task_id': task_id,
        'status': task_result.status,
        'result': task_result.result,
    }
    return JsonResponse(result)

def homepage(request):
    return render(request, 'home.html')

def upload_video(request):
    if request.method == 'POST':
        if 'video' not in request.FILES:
            return HttpResponseBadRequest("No video file uploaded")
        video = request.FILES['video']
        try:
            s3 = boto3.client('s3')
            s3.upload_fileobj(video, settings.AWS_STORAGE_BUCKET_NAME, video.name)
            task = process_video.delay(video.name)  # Start processing asynchronously
            
            return JsonResponse({'task_id': task.id})
        except Exception as e:
            return HttpResponseBadRequest(f"Error uploading video: {str(e)}")
    return render(request, 'upload.html')

def search(request):
    if 'q' in request.GET:
        keyword = request.GET['q']
        
        try:
            # Query DynamoDB for subtitles containing the keyword
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table(settings.DYNAMO_TABLE_NAME)
            
            response = table.scan(
                FilterExpression=Attr('subtitle_text').contains(keyword)
            )
            items = response['Items']
            return render(request, 'result.html', {'items': items})
        except Exception as e:
            return HttpResponseBadRequest(f"Error searching subtitles: {str(e)}")
    return render(request, 'search.html')
