"""stock URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
import django.urls
import django.views.generic
from django.contrib import admin
from django.urls import path
from user import views as userviews
from stockapi import views as stockviews

admin.site.site_title='股票数据采集和分析系统'
admin.site.site_header ='股票数据采集和分析系统'

urlpatterns = [
    # 网页图标
    path("favicon.ico", django.views.generic.RedirectView.as_view(url='static/fav.ico')),
    # user
    path('admin/', admin.site.urls),
    path('login/', userviews.loginPage,name='login'),
    path('logout/', userviews.logoutUser,name='logout'),
    path('register/', userviews.registerPage,name='register'),

    path('', userviews.indexPage,name='index'),
    path('index/<str:str>', userviews.indexPage, name='indexstr'),
    # stock
    path('details/', stockviews.detailsPage, name='details'),#默认股票页面
    path('details/<str:stockcode>', stockviews.detailsPage,name='details'),#输入参数查询指定股票
    # rank
    path('ranklist/', stockviews.ranklistPage, name='ranklist'),#默认排行榜页面
    path('ranklist/<str:str>/<str:type>/<int:pagenum>', stockviews.ranklistPage, name='ranklist'),
    path('ranktype/', stockviews.ranktypePage, name='ranktypeDefault'),#默认板块排行榜页面
    path('ranktype/<str:type>/<int:pagenum>', stockviews.ranktypePage, name='ranktype'),#获取参数实现分类排行
    path('ranktypelist/', stockviews.ranktypelistPage, name='ranktypelistDefault'),
    path('ranktypelist/<str:type>/<str:typeid>/<int:pagenum>', stockviews.ranktypelistPage, name='ranktypelist'),
    # namespaces
    path('user/', django.urls.include(('user.urls','user'), namespace='user')),
    path('stockapi/', django.urls.include(('stockapi.urls','stockapi'), namespace='stockapi')),
]
