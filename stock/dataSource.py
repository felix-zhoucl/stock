# -*- coding: utf-8 -*-
import datetime
import pymysql
import requests
import json
import logging

"""构建请求头"""

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104 Safari/537.36'
}

"""数据库配置"""

dbip = '127.0.0.1'  # 数据库IP地址
suname = 'root'  # 用户名
supwd = 'root'  # 密码
dbname = 'stockweb'  # 数据库名
chars = 'utf8'  # 编码格式

"""打印日志"""


def printlog(logFilename):
    """输出到文件的设置"""
    logging.basicConfig(
        level=logging.INFO,  # 定义输出到文件的log级别，大于此级别的都被输出
        format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
        datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
        filename='..//log/download/' + logFilename,  # log文件名
        filemode='a+')  # 写入模式
    """输出到控制台的句柄"""
    console = logging.StreamHandler()  # 定义console handler
    console.setLevel(logging.DEBUG)  # 定义该handler级别
    formatter = logging.Formatter('%(asctime)s  %(filename)s : %(levelname)s  %(message)s')  # 定义该handler格式
    console.setFormatter(formatter)
    logging.getLogger().addHandler(console)  # 实例化添加handler


"""更新数据"""


def daily():
    conn = pymysql.connect(
        host=dbip,
        user=suname, password=supwd,
        db=dbname,
        charset=chars)
    cursor = conn.cursor()
    try :
        sql = "select * from stockinfo order by date desc limit 0,1"  # 获取所有股票id，名称，代码
        cursor.execute(sql)
        data = cursor.fetchone()
        last_date = data[3]  # 最后一条数据的时间
        delta = datetime.timedelta(days=1)
        start_time = last_date + delta  # 延后一天
        start = start_time.strftime("%Y%m%d")
        current_date = datetime.datetime.now().date().strftime("%Y%m%d")
        printlog(current_date + 'download.log')  # 日志文件
        weekday = datetime.datetime.now().date().isoweekday()  # 今天星期几
        if (weekday > 5):
            # 周末不更新
            pass
            # print(start,current_date)
        else:
            # 交易日更新数据
            if (last_date == current_date):
                pass
            else:
                downLoadStockInfo(start, current_date)
                refreshRanklist()
    except Exception as e:
        logging.error(current_date+"更新失败")


# 股票交易数据
def downLoadStockInfo(starttime, endtime):
    conn = pymysql.connect(
        host=dbip,
        user=suname, password=supwd,
        db=dbname,
        charset=chars)
    cursor = conn.cursor()
    sql = "select stockid,stockname,stockcode from stocklist"  # 获取所有股票id，名称，代码
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        logging.info(results)
        rowcount = 0  # 股票计数
        for row in results:
            rowcount = rowcount + 1
            sid = row[0]  # 股票id
            sname = row[1]  # 股票名称
            scode = row[2]  # 股票代码
            url = 'http://quotes.money.163.com/service/chddata.html?code=' + sid + '&start=' + starttime + '&end=' + endtime
            response = requests.get(url, headers=headers)
            data = response.text  # 获取当前股票至今交易记录
            # print(data)
            datacount = data.count('\n')  # 统计行数
            insertcount = 0  # 统计已插入数量
            logging.info('开始第%s支股票%s%s共%s行数据' % (rowcount, sname, scode, datacount - 1))
            data = data.split('\n')
            for i in range(1, datacount):
                rowdata = data[i].split(',')
                try:
                    sql2 = "insert into stockinfo(date,stockcode,stockname,tclose,high,low,topen,lclose,chg,pchg,turnover,voturnover,vaturnover,tcap,mcap) " \
                           "values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
                           % (rowdata[0], scode, sname, rowdata[3], rowdata[4], rowdata[5], rowdata[6], rowdata[7],
                              rowdata[8], rowdata[9], rowdata[10], rowdata[11], rowdata[12], rowdata[13], rowdata[14])
                    sql2 = sql2.replace('nan', '0.0').replace('None', '0.0').replace('none', '0.0')  # 处理缺失值
                    cursor.execute(sql2)
                    conn.commit()
                    insertcount = insertcount + 1
                except Exception as e:
                    logging.error("插入第" + str(insertcount) + "条数据失败:", e)
            logging.info("第%s只股票%s共%s条数据，成功插入%s条" % (rowcount, sname, datacount - 1, insertcount))
    except Exception as e:
        logging.error("获取股票代码错误！:", e)


# 板块排行榜数据
def getRanklist(type):
    url = 'http://quotes.money.163.com/hs/realtimedata/service/plate.php?page=0&query=TYPE:' \
          + type + '&fields=RN,NAME,STOCK_COUNT,PERCENT,PLATE_ID,TYPE_CODE,PRICE,UPNUM,DOWNNUM,MAXPERCENTSTOCK,MINPERCENTSTOCK&sort=PERCENT&order=desc&count=all&type=query'
    response = requests.get(url, headers=headers)
    d = json.loads(response.text)
    logging.info("获取板块排行榜信息成功：" + type)
    # print(d)
    return d['list']


def refreshRanklist():
    dic = getRanklist('GAINIAN')
    dic1 = getRanklist('DIYU')
    dic2 = getRanklist('HANGYE')
    conn = pymysql.connect(
        host=dbip,
        user=suname, password=supwd,
        db=dbname,
        charset=chars)
    cursor = conn.cursor()
    sql = "select * from list_rank order by date desc limit 0,1"  # 获取所有股票id，名称，代码
    cursor.execute(sql)
    data = cursor.fetchone()
    last_date = data[1]  # 最后一条数据的时间
    delta = datetime.timedelta(days=1)
    start_time = last_date + delta  # 延后一天
    start = start_time.strftime("%Y%m%d")
    current_date = datetime.datetime.now().date().strftime("%Y%m%d")
    # try:
    if start == current_date:
        for row in (dic):
            # 空值处理
            if row['MAXPERCENTSTOCK'] == None:
                row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            if row['MINPERCENTSTOCK'] == None:
                row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            updatesql = "update list_rank set date=" + current_date + ",type='概念', name=" + row + ['NAME'] + \
                        ",typeid=row['PLATE_ID']," \
                        ",up=" + row['UPNUM'] + \
                        ",down=" + row['DOWNNUM'] + \
                        ",maxStockName=" + row['MAXPERCENTSTOCK']['NAME'] + \
                        ",maxStockPrice=" + row['MAXPERCENTSTOCK']['PRICE'] + \
                        ",maxStockPercent=" + round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2) + \
                        ",minStockName=" + row['MINPERCENTSTOCK']['NAME'] + \
                        ",minStockPrice=" + row['MINPERCENTSTOCK']['PRICE'] + \
                        ",minStockPercent=" + round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2) + \
                        ",avgPrice=" + round(row['PRICE'], 2) + \
                        ",avgPchg=" + round(row['PERCENT'] * 100, 2)
            cursor.execute(updatesql)
            conn.commit()
        for row in (dic1):
            if row['MAXPERCENTSTOCK'] == None:
                row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            if row['MINPERCENTSTOCK'] == None:
                row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            updatesql = "update list_rank set date=" + current_date + ",type='地域', name=" + row + ['NAME'] + \
                        ",typeid=row['PLATE_ID']," \
                        ",up=" + row['UPNUM'] + \
                        ",down=" + row['DOWNNUM'] + \
                        ",maxStockName=" + row['MAXPERCENTSTOCK']['NAME'] + \
                        ",maxStockPrice=" + row['MAXPERCENTSTOCK']['PRICE'] + \
                        ",maxStockPercent=" + round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2) + \
                        ",minStockName=" + row['MINPERCENTSTOCK']['NAME'] + \
                        ",minStockPrice=" + row['MINPERCENTSTOCK']['PRICE'] + \
                        ",minStockPercent=" + round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2) + \
                        ",avgPrice=" + round(row['PRICE'], 2) + \
                        ",avgPchg=" + round(row['PERCENT'] * 100, 2)
            cursor.execute(updatesql)
            conn.commit()
        for row in (dic2):
            if row['MAXPERCENTSTOCK'] == None:
                row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            if row['MINPERCENTSTOCK'] == None:
                row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            updatesql = "update list_rank set date=" + current_date + ",type='行业', name=" + row + ['NAME'] + \
                        ",typeid=row['PLATE_ID']," \
                        ",up=" + row['UPNUM'] + \
                        ",down=" + row['DOWNNUM'] + \
                        ",maxStockName=" + row['MAXPERCENTSTOCK']['NAME'] + \
                        ",maxStockPrice=" + row['MAXPERCENTSTOCK']['PRICE'] + \
                        ",maxStockPercent=" + round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2) + \
                        ",minStockName=" + row['MINPERCENTSTOCK']['NAME'] + \
                        ",minStockPrice=" + row['MINPERCENTSTOCK']['PRICE'] + \
                        ",minStockPercent=" + round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2) + \
                        ",avgPrice=" + round(row['PRICE'], 2) + \
                        ",avgPchg=" + round(row['PERCENT'] * 100, 2)
            cursor.execute(updatesql)
            conn.commit()
        logging.info(current_date + "更新成功")
    else:
        for row in (dic):
            if row['MAXPERCENTSTOCK'] == None:
                row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            if row['MINPERCENTSTOCK'] == None:
                row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            insertsql = "insert into list_rank " \
                        "(date,type,name,typeid,up,down,maxStockName,maxStockPrice,maxStockPercent,minStockName,minStockPrice,minStockPercent,avgPrice,avgPchg) " \
                        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (
                current_date,
                '概念',
                row['NAME'],
                row['PLATE_ID'],
                row['UPNUM'],
                row['DOWNNUM'],
                row['MAXPERCENTSTOCK']['NAME'],
                row['MAXPERCENTSTOCK']['PRICE'],
                round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                row['MINPERCENTSTOCK']['NAME'],
                row['MINPERCENTSTOCK']['PRICE'],
                round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                round(row['PRICE'], 2),
                round(row['PERCENT'] * 100, 2)
            )
            cursor.execute(insertsql, val)
            conn.commit()
        for row in (dic1):
            if row['MAXPERCENTSTOCK'] == None:
                row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            if row['MINPERCENTSTOCK'] == None:
                row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            insertsql = "insert into list_rank " \
                        "(date,type,name,typeid,up,down,maxStockName,maxStockPrice,maxStockPercent,minStockName,minStockPrice,minStockPercent,avgPrice,avgPchg) " \
                        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (
                current_date,
                '地域',
                row['NAME'],
                row['PLATE_ID'],
                row['UPNUM'],
                row['DOWNNUM'],
                row['MAXPERCENTSTOCK']['NAME'],
                row['MAXPERCENTSTOCK']['PRICE'],
                round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                row['MINPERCENTSTOCK']['NAME'],
                row['MINPERCENTSTOCK']['PRICE'],
                round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                round(row['PRICE'], 2),
                round(row['PERCENT'] * 100, 2)
            )
            cursor.execute(insertsql, val)
            conn.commit()
        for row in (dic2):
            if row['MAXPERCENTSTOCK'] == None:
                row['MAXPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            if row['MINPERCENTSTOCK'] == None:
                row['MINPERCENTSTOCK'] = {'NAME': "暂无", 'PERCENT': 0, 'PRICE': 0}
            insertsql = "insert into list_rank " \
                        "(date,type,name,typeid,up,down,maxStockName,maxStockPrice,maxStockPercent,minStockName,minStockPrice,minStockPercent,avgPrice,avgPchg) " \
                        "values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (
                current_date,
                '行业',
                row['NAME'],
                row['PLATE_ID'],
                row['UPNUM'],
                row['DOWNNUM'],
                row['MAXPERCENTSTOCK']['NAME'],
                row['MAXPERCENTSTOCK']['PRICE'],
                round(row['MAXPERCENTSTOCK']['PERCENT'] * 100, 2),
                row['MINPERCENTSTOCK']['NAME'],
                row['MINPERCENTSTOCK']['PRICE'],
                round(row['MINPERCENTSTOCK']['PERCENT'] * 100, 2),
                round(row['PRICE'], 2),
                round(row['PERCENT'] * 100, 2)
            )
            cursor.execute(insertsql, val)
            conn.commit()
        logging.info(current_date + "排行榜插入成功")
        # except Exception as e:
        #     logging.error(current_date+"排行榜更新失败")


"""主函数"""

if __name__ == '__main__':
    pass
    # printlog('download')
    # downLoadStockInfo()
    daily()
    # refreshRanklist()
