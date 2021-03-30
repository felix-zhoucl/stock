import django.urls
from django.urls import path
from user import views


urlpatterns = [
    path('checkUsername', views.checkUsername,name='checkUsername'),
    path('checkEmail', views.checkEmail, name='checkEmail'),
    path('checkPass', views.checkPass, name='checkPass'),
    path('getfav', views.getfav, name='getfav'),
]
