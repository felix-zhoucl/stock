from django.contrib import admin
from djangoql.admin import DjangoQLSearchMixin
from .models import stocklist, stockinfo, hangye, diyu, gainian, typeRanklist
from django.utils import timezone
import json
import requests
import logging

logger = logging.getLogger("django.request")

# 爬虫
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}

# 板块列表
def getTypelist(type):
    url = 'http://quotes.money.163.com/hs/realtimedata/service/plate.php?query=TYPE:' \
          + type + '&fields=NAME,STOCK_COUNT,PLATE_ID,&count=all'
    response = requests.get(url, headers=headers)
    d = json.loads(response.text)
    logger.info("获取板块列表成功："+type)
    # print(d)
    return d['list']

# 某板块内股票列表
def getStocklist(typeid):
    url = 'http://quotes.money.163.com/hs/service/diyrank.php?query=' \
          'PLATE_IDS:' + typeid + '&fields=SYMBOL,NAME,CODE,&count=all'
    response = requests.get(url, headers=headers)
    d = json.loads(response.text)
    logger.info("获取板块信息成功："+typeid)
    return d['list']

# 板块排行榜数据
def getRanklist(type):
    url = 'http://quotes.money.163.com/hs/realtimedata/service/plate.php?page=0&query=TYPE:' \
          + type + '&fields=RN,NAME,STOCK_COUNT,PERCENT,PLATE_ID,TYPE_CODE,PRICE,UPNUM,DOWNNUM,MAXPERCENTSTOCK,MINPERCENTSTOCK&sort=PERCENT&order=desc&count=all&type=query'
    response = requests.get(url, headers=headers)
    d = json.loads(response.text)
    logger.info("获取板块排行榜信息成功："+type)
    # print(d)
    return d['list']


# 股票信息表
class stocklistAdmin(admin.ModelAdmin):
    list_display = ('stockid', 'stockcode', 'stockname', 'hangye', 'gainian', 'diyu', 'time')
    list_per_page = 12
    list_filter = ('hangye','gainian','diyu')
    search_fields = ('stockcode',)
    # 更新按钮
    actions = ['refreshStockList']

    def refreshStockList(self, request, queryset):
        try:
            hangyeL = list(hangye.objects.all())
            for h in hangyeL:
                stockL = getStocklist(str(h.code))
                for s in stockL:
                    obj, created = stocklist.objects.update_or_create(
                        stockcode=s['SYMBOL'], stockid=s['CODE'],
                        defaults={'stockid': s['CODE'], 'stockcode': s['SYMBOL'], 'stockname': s['NAME'], 'hangye': h.name})
            diyuL = list(diyu.objects.all())
            for h in diyuL:
                stockL = getStocklist(str(h.code))
                for s in stockL:
                    obj, created = stocklist.objects.update_or_create(
                        stockcode=s['SYMBOL'], stockid=s['CODE'],
                        defaults={'stockid': s['CODE'], 'stockcode': s['SYMBOL'], 'stockname': s['NAME'], 'diyu': h.name})
            gainianL = list(gainian.objects.all())
            for h in gainianL:
                stockL = getStocklist(str(h.code))
                for s in stockL:
                    obj, created = stocklist.objects.update_or_create(
                        stockcode=s['SYMBOL'], stockid=s['CODE'],
                        defaults={'stockid': s['CODE'], 'stockcode': s['SYMBOL'], 'stockname': s['NAME'],
                                  'gainian': h.name})
            self.message_user(request, "更新成功", 'success')
        except Exception as e:
            self.message_user(request, "出错了，更新失败", 'error')

    refreshStockList.icon = 'fas fa-sync-alt'
    refreshStockList.short_description = ' 更新'
    refreshStockList.type = 'success'


admin.site.register(stocklist, stocklistAdmin)


# 交易信息表
class stockinfoAdmin(DjangoQLSearchMixin, admin.ModelAdmin):
    list_display = ('date', 'stockcode', 'stockname', 'topen', 'tclose', 'chg', 'pchg')
    # search_fields = ("stockcode", "stockname", )
    # search_fields = ('stockcode', 'stockname',)
    search_field = "my search query"
    # date_hierarchy = 'date'
    show_full_result_count = False
    # paginator = DumbPaginator
    ordering = ('-date',)
    list_per_page = 30


admin.site.register(stockinfo, stockinfoAdmin)


# 行业表
class hangyeAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'count', 'time',)
    list_per_page = 12
    search_fields = ('code', 'name',)
    # 更新按钮
    actions = ['refreshHangyeList']

    def refreshHangyeList(self, request, queryset):
        dic = getTypelist('HANGYE')
        try:
            for row in (dic):
                obj, created = hangye.objects.update_or_create(
                    code=row['PLATE_ID'],
                    defaults={'code': row['PLATE_ID'], 'name': row['NAME'], 'count': row['STOCK_COUNT']})
            self.message_user(request, "更新成功", 'success')
        except Exception as e:
            self.message_user(request, "更新列表失败", 'error')
    refreshHangyeList.icon = 'fas fa-sync-alt'
    refreshHangyeList.short_description = ' 更新'
    refreshHangyeList.type = 'success'


admin.site.register(hangye, hangyeAdmin)


# 地域表
class diyuAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'count', 'time',)
    list_per_page = 12
    search_fields = ('code', 'name',)
    # 更新按钮
    actions = ['refreshDiyuList']

    def refreshDiyuList(self, request, queryset):
        dic = getTypelist('DIYU')
        try:
            for row in (dic):
                obj, created = diyu.objects.update_or_create(
                    code=row['PLATE_ID'],
                    defaults={'code': row['PLATE_ID'], 'name': row['NAME'], 'count': row['STOCK_COUNT']})
            self.message_user(request, "更新成功", 'success')
        except Exception as e:
            self.message_user(request, "更新列表失败", 'error')

    refreshDiyuList.icon = 'fas fa-sync-alt'
    refreshDiyuList.short_description = ' 更新'
    refreshDiyuList.type = 'success'


admin.site.register(diyu, diyuAdmin)


# 概念表
class gainianAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'count', 'time',)
    list_per_page = 12
    search_fields = ('code', 'name',)
    # 更新按钮
    actions = ['refreshGainianList']

    def refreshGainianList(self, request, queryset):
        dic = getTypelist('GAINIAN')
        try:
            for row in (dic):
                obj, created = gainian.objects.update_or_create(
                    code=row['PLATE_ID'],
                    defaults={'code': row['PLATE_ID'], 'name': row['NAME'], 'count': row['STOCK_COUNT']})
            self.message_user(request, "更新成功", 'success')
        except Exception as e:
            self.message_user(request, "更新列表失败", 'error')
    refreshGainianList.icon = 'fas fa-sync-alt'
    refreshGainianList.short_description = ' 更新'
    refreshGainianList.type = 'success'


admin.site.register(gainian, gainianAdmin)


# paihang
class rankAdmin(admin.ModelAdmin):
    list_display = ('date', 'type', 'name', 'up', 'down',
                    'maxStockName','maxStockPrice','maxStockPercent',
                    'minStockName','minStockPrice','minStockPercent',
                    'avgPrice', 'avgPchg')
    list_per_page = 12
    list_filter = ('type',)
    search_fields = ('name',)
    date_hierarchy = 'date'
    ordering = ('-date',)
    # 更新按钮
    actions = ['refreshRankList']

    def refreshRankList(self, request, queryset):
        create_date = timezone.localtime().date()
        last_date = typeRanklist.objects.last().date
        dic = getRanklist('GAINIAN')
        dic1 = getRanklist('DIYU')
        dic2 = getRanklist('HANGYE')
        try :
            if last_date == create_date:
                for row in (dic):
                    if row['MAXPERCENTSTOCK']==None:
                        row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    if row['MINPERCENTSTOCK'] == None:
                        row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    typeRanklist.objects.filter(date=create_date, typeid=row['PLATE_ID']).update(
                        date=create_date,
                        type='概念',
                        name=row['NAME'],
                        typeid=row['PLATE_ID'],
                        up=row['UPNUM'],
                        down=row['DOWNNUM'],
                        maxStockName=row['MAXPERCENTSTOCK']['NAME'],
                        maxStockPrice = row['MAXPERCENTSTOCK']['PRICE'],
                        maxStockPercent =round(row['MAXPERCENTSTOCK']['PERCENT']*100,2),
                        minStockName = row['MINPERCENTSTOCK']['NAME'],
                        minStockPrice = row['MINPERCENTSTOCK']['PRICE'],
                        minStockPercent = round(row['MINPERCENTSTOCK']['PERCENT']*100,2),
                        avgPrice=round(row['PRICE'],2),
                        avgPchg=round(row['PERCENT']*100,2)
                    )
                for row in (dic1):
                    if row['MAXPERCENTSTOCK']==None:
                        row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    if row['MINPERCENTSTOCK'] == None:
                        row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    typeRanklist.objects.filter(date=create_date, typeid=row['PLATE_ID']).update(
                        date=create_date,
                        type='地域',
                        name=row['NAME'],
                        typeid=row['PLATE_ID'],
                        up=row['UPNUM'],
                        down=row['DOWNNUM'],
                        maxStockName=row['MAXPERCENTSTOCK']['NAME'],
                        maxStockPrice=row['MAXPERCENTSTOCK']['PRICE'],
                        maxStockPercent=round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                        minStockName=row['MINPERCENTSTOCK']['NAME'],
                        minStockPrice=row['MINPERCENTSTOCK']['PRICE'],
                        minStockPercent=round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                        avgPrice=round(row['PRICE'], 2),
                        avgPchg=round(row['PERCENT'] * 100, 2)
                    )
                for row in (dic2):
                    if row['MAXPERCENTSTOCK']==None:
                        row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    if row['MINPERCENTSTOCK'] == None:
                        row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    typeRanklist.objects.filter(date=create_date, typeid=row['PLATE_ID']).update(
                        date=create_date,
                        type='行业',
                        name=row['NAME'],
                        typeid=row['PLATE_ID'],
                        up=row['UPNUM'],
                        down=row['DOWNNUM'],
                        maxStockName=row['MAXPERCENTSTOCK']['NAME'],
                        maxStockPrice=row['MAXPERCENTSTOCK']['PRICE'],
                        maxStockPercent=round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                        minStockName=row['MINPERCENTSTOCK']['NAME'],
                        minStockPrice=row['MINPERCENTSTOCK']['PRICE'],
                        minStockPercent=round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                        avgPrice=round(row['PRICE'], 2),
                        avgPchg=round(row['PERCENT'] * 100, 2)
                    )
                self.message_user(request, "更新成功", 'success')
            else:
                for row in (dic):
                    if row['MAXPERCENTSTOCK']==None:
                        row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    if row['MINPERCENTSTOCK'] == None:
                        row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    newrank = typeRanklist(
                        date=create_date,
                        type='概念',
                        name=row['NAME'],
                        typeid=row['PLATE_ID'],
                        up=row['UPNUM'],
                        down=row['DOWNNUM'],
                        maxStockName=row['MAXPERCENTSTOCK']['NAME'],
                        maxStockPrice=row['MAXPERCENTSTOCK']['PRICE'],
                        maxStockPercent=round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                        minStockName=row['MINPERCENTSTOCK']['NAME'],
                        minStockPrice=row['MINPERCENTSTOCK']['PRICE'],
                        minStockPercent=round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                        avgPrice=round(row['PRICE'], 2),
                        avgPchg=round(row['PERCENT'] * 100, 2)
                    )
                    newrank.save()
                for row in (dic1):
                    if row['MAXPERCENTSTOCK']==None:
                        row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    if row['MINPERCENTSTOCK'] == None:
                        row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    newrank = typeRanklist(
                        date=create_date,
                        type='地域',
                        name=row['NAME'],
                        typeid=row['PLATE_ID'],
                        up=row['UPNUM'],
                        down=row['DOWNNUM'],
                        maxStockName=row['MAXPERCENTSTOCK']['NAME'],
                        maxStockPrice=row['MAXPERCENTSTOCK']['PRICE'],
                        maxStockPercent=round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                        minStockName=row['MINPERCENTSTOCK']['NAME'],
                        minStockPrice=row['MINPERCENTSTOCK']['PRICE'],
                        minStockPercent=round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                        avgPrice=round(row['PRICE'], 2),
                        avgPchg=round(row['PERCENT'] * 100, 2)
                    )
                    newrank.save()
                for row in (dic2):
                    if row['MAXPERCENTSTOCK']==None:
                        row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    if row['MINPERCENTSTOCK'] == None:
                        row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
                    newrank = typeRanklist(
                        date=create_date,
                        type='行业',
                        name=row['NAME'],
                        typeid=row['PLATE_ID'],
                        up=row['UPNUM'],
                        down=row['DOWNNUM'],
                        maxStockName=row['MAXPERCENTSTOCK']['NAME'],
                        maxStockPrice=row['MAXPERCENTSTOCK']['PRICE'],
                        maxStockPercent=round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                        minStockName=row['MINPERCENTSTOCK']['NAME'],
                        minStockPrice=row['MINPERCENTSTOCK']['PRICE'],
                        minStockPercent=round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                        avgPrice=round(row['PRICE'], 2),
                        avgPchg=round(row['PERCENT'] * 100, 2)
                    )
                    newrank.save()
                self.message_user(request, "新增成功", 'success')
        except Exception as e:
            self.message_user(request, "刷新列表失败", 'error')

    refreshRankList.icon = 'fas fa-sync-alt'
    refreshRankList.short_description = ' 更新'
    refreshRankList.type = 'success'


admin.site.register(typeRanklist, rankAdmin)
