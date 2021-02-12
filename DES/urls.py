"""DES URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls. static import static
from django.contrib import staticfiles


'''
from django.conf.urls import handler404, handler500

handler404 = "DES1.views.page_not_found"
handler500 = "DES1.views.page_error"
'''

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('DES1.urls')),
    path('index/',include("uploadFile.urls")),

]+ static (settings.STATIC_URL, document_root = settings.STATIC_ROOT)
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('DES1.urls')),
    path('index/',include("uploadFile.urls")),

    url(r'^static/(?P<path>.*)$', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
]
'''
