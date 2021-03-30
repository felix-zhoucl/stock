from django.db import models

# Create your models here.

# class myUser(models.Model):
#     username = models.CharField(max_length=20, unique=True, verbose_name='用户名称')
#     password = models.CharField(max_length=40, verbose_name='用户密码')
#     email = models.EmailField(unique=True,verbose_name='用户邮箱')
#     is_active = models.BooleanField(default=True, verbose_name='激活状态')
#     class Meta:
#        db_table = 'myuser'
class stocklist(models.Model):
    stockid = models.CharField(max_length=10,unique=True,verbose_name='股票id')
    stockname = models.CharField(max_length=10,verbose_name='股票名称')
    stockcode = models.CharField(max_length=10,unique=True,verbose_name='股票代码')
    hangye = models.CharField(max_length=10,verbose_name='行业',blank=True)
    gainian = models.CharField(max_length=10,verbose_name='概念',blank=True)
    diyu = models.CharField(max_length=10,verbose_name='地域',blank=True)
    time = models.DateTimeField(auto_now=True,verbose_name='最后更新时间')
    class Meta:
        db_table = 'stocklist'
        verbose_name_plural = '股票列表'

class stockinfo(models.Model):
    stockname = models.CharField(max_length=10, verbose_name='股票名称')
    stockcode = models.CharField(max_length=10, db_index=True,unique=False, verbose_name='股票代码')
    date = models.DateField(db_index=True,blank=True,verbose_name='交易日期')
    tclose = models.FloatField(verbose_name='今收盘')
    high = models.FloatField(verbose_name='最高价')
    low = models.FloatField(verbose_name='最低价')
    topen = models.FloatField(verbose_name='今开盘')
    lclose = models.FloatField(verbose_name='前收盘')
    chg = models.FloatField(verbose_name='涨跌额')
    pchg = models.FloatField(verbose_name='涨跌幅')
    turnover = models.FloatField(verbose_name='换手率')
    voturnover = models.BigIntegerField(verbose_name='成交量')
    vaturnover = models.BigIntegerField(verbose_name='成交金额')
    tcap = models.BigIntegerField(verbose_name='总市值')
    mcap = models.BigIntegerField(verbose_name='流通市值')
    class Meta:
        db_table = 'stockinfo'
        verbose_name_plural = '交易数据'

class hangye(models.Model):
    name = models.CharField(max_length=15, verbose_name='行业名称')
    code = models.CharField(max_length=10, db_index=True,unique=True, verbose_name='行业代码')
    count = models.IntegerField(null=True,verbose_name='数量')
    time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    class Meta:
        db_table = 'list_hangye'
        verbose_name_plural = '行业列表'

class gainian(models.Model):
    name = models.CharField(max_length=15, verbose_name='概念名称')
    code = models.CharField(max_length=10, db_index=True,unique=True, verbose_name='概念代码')
    count = models.IntegerField(null=True, verbose_name='数量')
    time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    class Meta:
        db_table = 'list_gainian'
        verbose_name_plural = '概念列表'

class diyu(models.Model):
    name = models.CharField(max_length=15, verbose_name='地域名称')
    code = models.CharField(max_length=10, db_index=True,unique=True, verbose_name='地域代码')
    count = models.IntegerField(null=True,verbose_name='数量')
    time = models.DateTimeField(auto_now=True, verbose_name='最后更新时间')
    class Meta:
        db_table = 'list_diyu'
        verbose_name_plural = '地域列表'

class typeRanklist(models.Model):
    date = models.DateField(db_index=True, blank=True, verbose_name='交易日期')
    type = models.CharField(max_length=15, verbose_name='板块分类')
    name = models.CharField(max_length=15, verbose_name='板块名称')
    typeid = models.CharField(max_length=15,blank=True, verbose_name='板块代码')
    up =  models.IntegerField(null=True,verbose_name='上涨数')
    down = models.IntegerField(null=True, verbose_name='下跌数')
    maxStockName = models.CharField(max_length=15, verbose_name='领涨股票')
    maxStockPrice = models.FloatField(verbose_name='领涨价格')
    maxStockPercent = models.FloatField(verbose_name='领涨幅度')
    minStockName = models.CharField(max_length=15, verbose_name='领跌股票')
    minStockPrice = models.FloatField(verbose_name='领跌价格')
    minStockPercent = models.FloatField(verbose_name='领跌幅度')
    avgPrice = models.FloatField(verbose_name='平均价格')
    avgPchg = models.FloatField(verbose_name='平均涨跌幅')
    class Meta:
        db_table = 'list_rank'
        verbose_name_plural = '板块排行榜'

class predict(models.Model):
    stockcode = models.CharField(max_length=10, db_index=True, unique=False, verbose_name='股票代码')
    predic = models.TextField(verbose_name='数值')

    class Meta:
        db_table = 'prediction'
        verbose_name_plural = '预测'