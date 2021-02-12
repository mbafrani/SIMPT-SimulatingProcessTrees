from django.urls import path
from . import views

app_name = 'upload'
urlpatterns = [
 path('file/',views.userfile,name='userfile'),
 path('file/detail/',views.detailFile,name='delfile'),
]
