from django.urls import path
from .views import upload_video, search, homepage, check_task_status

urlpatterns = [
    path('', homepage, name='homepage'),
    path('upload/', upload_video, name='upload'),
    path('search/', search, name='search'),
    path('task-status/<str:task_id>/', check_task_status, name='check_task_status'),
]
