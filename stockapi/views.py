from django.core import serializers
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q

import re

import datetime

from .models import stocklist,stockinfo,hangye,gainian,diyu,predict
from user.models import user_stock
from django.contrib.auth.models import User
import json

from .models import typeRanklist
# Create your views here.

# 股票详情页
def detailsPage(request,stockcode='601318'):
    # 最新交易信息
    stock = stockinfo.objects.filter(stockcode=stockcode).order_by('-date').first()
    # 所有交易信息
    history = stockinfo.objects.filter(stockcode=stockcode).order_by('date')
    # 股票基本信息
    info =stocklist.objects.filter(stockcode=stockcode).first()
    # 预测信息
    pre=[]
    try:
        pre= predict.objects.filter(stockcode=stockcode).first()
        pre=pre.predic
        pre=pre.replace('  ',' ')
        pre = pre.replace('  ', ' ')
        pre = pre.replace(' ', ',')
        # print("pre:",pre)
    except:
        pre=stockinfo.objects.filter(stockcode=stockcode).order_by('-date').first().topen
    context={
        "stock":stock,
        "info":info,
        "history":history,
        "pre":pre
    }
    return render(request,'stockinfo/details.html',context)

# 板块排行页
def ranktypePage(request,type='hangye',pagenum=1):
    ranktype=type+'Rank()'
    last_date = typeRanklist.objects.last().date
    if type=='hangye':
        ranklist=typeRanklist.objects.filter(type='行业',date=last_date).order_by('-avgPchg')
    if type=='diyu':
        ranklist = typeRanklist.objects.filter(type='地域', date=last_date).order_by('-avgPchg')
    if type=='gainian':
        ranklist = typeRanklist.objects.filter(type='概念', date=last_date).order_by('-avgPchg')
    paginator= Paginator(ranklist,15)
    page=paginator.page(pagenum)
    context={"page":page,"ranktype":ranktype,"type":type}
    return render(request,'stockinfo/ranktype.html',context)


# 详细板块排行
def ranktypelistPage(request,type='hangye',typeid='hy001000',pagenum=1):
    ranktype=type+'Rank()'
    last_date = stockinfo.objects.last().date
    if type=='hangye':
        hangyeName=hangye.objects.filter(code=typeid).first().name
        liststock=stocklist.objects.values("stockcode").filter(hangye=hangyeName)
        ranklist=stockinfo.objects.filter(stockcode__in=liststock,date=last_date).order_by('-pchg')
        menu=hangye.objects.all()
    if type=='diyu':
        diyuName = diyu.objects.filter(code=typeid).first().name
        liststock = stocklist.objects.values("stockcode").filter(diyu=diyuName)
        ranklist = stockinfo.objects.filter(stockcode__in=liststock, date=last_date).order_by('-pchg')
        menu = diyu.objects.all()
    if type=='gainian':
        gainianName = gainian.objects.filter(code=typeid).first().name
        liststock = stocklist.objects.values("stockcode").filter(gainian=gainianName)
        ranklist = stockinfo.objects.filter(stockcode__in=liststock, date=last_date).order_by('-pchg')
        menu = gainian.objects.all()
    paginator= Paginator(ranklist,15)
    page=paginator.page(pagenum)
    context={"page":page,"ranktype":ranktype,"type":type,"typeid":typeid,"menu":menu}
    return render(request,'stockinfo/ranktypelist.html',context)


# 详细涨跌排行
def ranklistPage(request,str='',type='zhangfu',pagenum=1):
    last_date = stockinfo.objects.last().date
    if (str == ''or str=='hsa'):  # 默认
        if (type=='zhangfu'):
            ranklist = stockinfo.objects.filter(date=last_date).order_by('-pchg')[:150]
        if (type == 'diefu'):
            ranklist = stockinfo.objects.filter(date=last_date).order_by('pchg')[:150]
        if (type == 'chengjiaoe'):
            ranklist = stockinfo.objects.filter(date=last_date).order_by('-vaturnover')[:150]
        if (type == 'chengjiaoliang'):
            ranklist = stockinfo.objects.filter(date=last_date).order_by('-voturnover')[:150]
        str='hsa'
    if (str == 'sha'):  # 上证A股
        code = '600'
        code2='601'
        code3='603'
        if (type=='zhangfu'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('-pchg')[:150]
        if (type == 'diefu'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('pchg')[:150]
        if (type == 'chengjiaoe'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('-vaturnover')[:150]
        if (type == 'chengjiaoliang'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('-voturnover')[:150]
    if (str == 'sza'):  # 深圳A股
        code = '000'
        if (type == 'zhangfu'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-pchg')[:150]
        if (type == 'diefu'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('pchg')[:150]
        if (type == 'chengjiaoe'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-vaturnover')[:150]
        if (type == 'chengjiaoliang'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-voturnover')[:150]
    if (str == 'zxb'):  # 中小板
        code = '002'
        if (type == 'zhangfu'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-pchg')[:150]
        if (type == 'diefu'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('pchg')[:150]
        if (type == 'chengjiaoe'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-vaturnover')[:150]
        if (type == 'chengjiaoliang'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-voturnover')[:150]
    if (str == 'kcb'):  # 科创板
        code = '688'
        if (type == 'zhangfu'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-pchg')[:150]
        if (type == 'diefu'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('pchg')[:150]
        if (type == 'chengjiaoe'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-vaturnover')[:150]
        if (type == 'chengjiaoliang'):
            ranklist = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-voturnover')[:150]
    if (str == 'hsb'):  # 沪深B股
        code = '200'
        code2 = '900'
        if (type == 'zhangfu'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('-pchg')[:150]
        if (type == 'diefu'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('pchg')[:150]
        if (type == 'chengjiaoe'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('-vaturnover')[:150]
        if (type == 'chengjiaoliang'):
            ranklist = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('-voturnover')[:150]
    paginator= Paginator(ranklist,15)
    page=paginator.page(pagenum)
    context={"page":page,"str":str,"type":type}
    return render(request,'stockinfo/ranklist.html',context)

def getRankList(request):
    last_date = typeRanklist.objects.last().date
    hangye = serializers.serialize("json", typeRanklist.objects.filter(type='行业',date=last_date).order_by('-avgPchg')[:5])
    diyu = serializers.serialize("json", typeRanklist.objects.filter(type='地域', date=last_date).order_by('-avgPchg')[:5])
    gainian = serializers.serialize("json", typeRanklist.objects.filter(type='概念', date=last_date).order_by('-avgPchg')[:5])

    data = {
        'hangye': hangye,
        'gainian': gainian,
        'diyu': diyu,
        'status': 'ok'}
    return HttpResponse(json.dumps(data))

def search(request):
    if request.method=='POST':
        searchfields = request.POST.get('stock',None)
        data={
            'statuscode':0,
            'status':'falied',
            'list':[],
        }
        exist = stocklist.objects.filter(Q(stockcode__icontains=searchfields)|Q(stockname__icontains=searchfields))[:6]
        list =  serializers.serialize("json",exist)
        if exist:
            data['statuscode']=1
            data['status']='ok'
            data['list'] = list
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))


def follow(request):
    if request.method=='POST':
        stockname = request.POST.get('stock',None)      #股票名
        username = request.user.username  # 用户名
        isFollowed = user_stock.objects.filter(stockname=stockname,username=username)  #是否已关注
        try:
            if(isFollowed):
                # print("delete")
                user_stock.objects.filter(stockname=stockname,username=username).delete()
            else:
                user=User.objects.filter(username=username).first()
                stock=stocklist.objects.filter(stockname=stockname).first()
                fav=user_stock(
                    userid=user.id,
                    username=user,
                    stockcode=stock.stockcode,
                    stockname=stock.stockname)
                fav.save()
                # print(stock.stockname,user.id)
            data={
                'statuscode':1,
                'status':'ok',
            }
            return HttpResponse(json.dumps(data))
        except :
            data = {
                'statuscode': 0,
                'status': 'falied',
            }
            return HttpResponse(json.dumps(data))