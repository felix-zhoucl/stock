# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import validate_email
from django.core import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, login, logout
import json
import logging
from django.db.models import Q
from stockapi.models import stockinfo
from .models import user_stock

logger = logging.getLogger("django.request")

from .utils.customErrorMessage import CustomErrorList
from .forms import createUserForm

'''注册页面'''


def registerPage(request):
    # form = createUserForm()
    logger.info(request)
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = createUserForm(request.POST, error_class=CustomErrorList)
        # form = createUserForm(request.POST,)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + '注册成功')

            return redirect('/login')
        else:
            print(form.errors)
    else:
        form = createUserForm()
    context = {'form': form}
    return render(request, 'account/register.html', context)


# 用户名校验


def checkUsername(request):
    if request.method == 'POST':
        username = request.POST.get('username', None)
        # is_available = request.POST.get('is_available',None)
        data = {'statuscode': 1, 'status': 'ok'}
        exist = User.objects.filter(username=username)
        if exist:
            data['statuscode'] = 0
            data['status'] = 'failed'
            return HttpResponse(json.dumps(data))
        else:
            return HttpResponse(json.dumps(data))
    else:
        return registerPage(request)


# 邮箱地址格式校验


def checkEmail(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        data = {'statuscode': 1, 'status': 'ok'}
        try:
            validate_email(email)
            return HttpResponse(json.dumps(data))
        except:
            data['statuscode'] = 0
            data['status'] = 'failed'
            return HttpResponse(json.dumps(data))
    else:
        return registerPage(request)


# 密码复杂度校验


def checkPass(request):
    if request.method == 'POST':
        user = request.POST.get('user', None)
        pwd = request.POST.get('pwd', None)
        data = {'statuscode': 1, 'status': 'ok', 'errors': 'error'}
        try:
            validate_password(pwd, user)
            return HttpResponse(json.dumps(data))
        except ValidationError as error:
            data['statuscode'] = 0
            data['status'] = 'failed'
            data['errors'] = str(error)
            # print(error)
            return HttpResponse(json.dumps(data))
    else:
        return registerPage(request)


'''主页'''


# @login_required
def indexPage(request, str=''):
    logger.info(request)
    last_date = stockinfo.objects.last().date
    zhangfu=[]
    diefu=[]
    vaturnover=[]
    voturnover=[]
    ranktype=''
    if (str == ''):  # 默认
        zhangfu = stockinfo.objects.filter(date=last_date).order_by('-pchg')[:10]
        diefu = stockinfo.objects.filter(date=last_date).order_by('pchg')[:10]
        vaturnover = stockinfo.objects.filter(date=last_date).order_by('-vaturnover')[:10]
        voturnover = stockinfo.objects.filter(date=last_date).order_by('-voturnover')[:10]
        str='hsa'
    if (str == 'sha'):  # 上证A股
        code = '600'
        code2='601'
        code3='603'
        zhangfu = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('-pchg')[:10]
        diefu = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('pchg')[:10]
        vaturnover = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('-vaturnover')[:10]
        voturnover = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)|Q(date=last_date, stockcode__startswith=code3)).order_by('-voturnover')[:10]
    if (str == 'sza'):  # 深圳A股
        code = '000'
        zhangfu = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-pchg')[:10]
        diefu = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('pchg')[:10]
        vaturnover = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-vaturnover')[:10]
        voturnover = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-voturnover')[:10]

    if (str == 'zxb'):  # 中小板
        code = '002'
        zhangfu = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-pchg')[:10]
        diefu = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('pchg')[:10]
        vaturnover = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-vaturnover')[:10]
        voturnover = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-voturnover')[:10]

    if (str == 'kcb'):  # 科创板
        code = '688'
        zhangfu = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-pchg')[:10]
        diefu = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('pchg')[:10]
        vaturnover = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-vaturnover')[:10]
        voturnover = stockinfo.objects.filter(date=last_date, stockcode__startswith=code).order_by('-voturnover')[:10]
        ranktype = str+'()'
    if (str == 'hsb'):  # 沪深B股
        code = '200'
        code2 = '900'
        zhangfu = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('-pchg')[:10]
        diefu = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('pchg')[:10]
        vaturnover = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('-vaturnover')[:10]
        voturnover = stockinfo.objects.filter(Q(date=last_date, stockcode__startswith=code)|Q(date=last_date, stockcode__startswith=code2)).order_by('-voturnover')[:10]

    context = {
        "zhangfu": zhangfu,
        "diefu": diefu,
        "vo": voturnover,
        "va": vaturnover,
        "str": str,
    }
    return render(request, 'index.html', context)


'''登录页'''


def loginPage(request):
    logger.info(request)
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['islogin'] = True
            request.session['username'] = username
            # request.session['favorite'] = serializers.serialize("json", user_stock.objects.filter(username=username))
            return redirect('/')
        else:
            messages.info(request, '用户名或密码错误！')
            return render(request, 'account/login.html')
    return render(request, 'account/login.html')


'''登出'''


def logoutUser(request):
    logger.info(request)
    logout(request)
    return indexPage(request)


# 获取收藏列表
def getfav(request):
    username = request.session.get('username')
    # print(username)
    fav = serializers.serialize("json", user_stock.objects.filter(username=username))
    return HttpResponse(fav)
