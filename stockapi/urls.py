import django.urls
from django.urls import path
from stockapi import views


urlpatterns = [
    path('getRankList', views.getRankList,name='getRankList'),
    path('search', views.search,name='search'),
    path('follow', views.follow,name='follow'),

]
