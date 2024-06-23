from django.urls import path
from .views import upload_video, search, homepage

urlpatterns = [
    path('', homepage, name='homepage'),
    path('upload/', upload_video, name='upload'),
    path('search/', search, name='search'),
]
