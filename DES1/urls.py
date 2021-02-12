from . import views
from django.urls import path
from django.conf.urls import url


urlpatterns = [

    path('',views.home,name="home"),
    path('config/',views.config,name="config"),
    path('result/',views.result,name="result"),
    path('simulation/',views.simulation,name="simulation"),
    path('overview/',views.overview,name="overview"),
    path('continuee/',views.continuee,name="continuee"),
    path('submit/',views.submit,name="submit"),
    path('record/',views.record,name="record"),
    path('save/',views.save,name="save"),
    path('result2/',views.result2,name="result2"),
    path('info/',views.info,name="info"),
    path('base2/',views.base2,name="base2"),
    path('base2/submit2/',views.submit2,name="submit2"),
    path('base2/submit3/',views.submit3,name="submit3"),
    path('setting/',views.setting,name="setting"),
    path('processtree/',views.processtree,name="processtree"),
    path('processtree/changep/',views.changeptree,name="changeptree"),
    path('statics/',views.statics,name="statics"),
    path('download/', views.DownLoadApiView, name="download"),




    #path('continue/',views.continue,name="continue")

]
