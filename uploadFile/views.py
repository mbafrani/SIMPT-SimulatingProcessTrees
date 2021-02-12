from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
import uuid,os
from .models import User

# Create your views here.
global logname

def userfile(request):
 return render(request,'uploadFile/uploadFile.html')
def detailFile(request):
 global logname
 if request.method == "POST":
  #name = 'input_log'
  file = request.FILES.get('file',None)
  logname=file.name
  if not file:
    return render(request,'home.html',{})
   #return HttpResponse("<p>Upload failed!</p>")
  file.name = 'input_log'+os.path.splitext(file.name)[1]
  #user = User.objects.create(name=name, file=file)

  #user = User.objects.create(name=name, file=file)
  with open(os.path.join("./media/log",file.name),'wb+') as relfile:
   for crunk in file.chunks():
    relfile.write(crunk)

  #driver = webdriver.Chrome()
  #driver.execute_script("window.alert('这是一个alert弹框。');")
  #alert("You choose YES! Great!")
  return render(request,'home.html',{})
  #return HttpResponse("<p>Upload successfully!</p>")

  #return HttpResponse("<script>alert('Submit successfully!');</script>")
  #return Response.Write(<script>alert("<p>ccc</p>")</script>)
 else:

  pass
def getUUID(filename):
 id = 'input_log'
 extend = os.path.splitext(filename)[1]
 return id+extend

def getlogname():
    return logname
