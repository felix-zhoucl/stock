# Generated by Django 3.0.5 on 2020-05-24 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='diyu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='地域名称')),
                ('code', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='地域代码')),
            ],
            options={
                'verbose_name_plural': '地域列表',
                'db_table': 'list_diyu',
            },
        ),
        migrations.CreateModel(
            name='gainian',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='概念名称')),
                ('code', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='概念代码')),
            ],
            options={
                'verbose_name_plural': '概念列表',
                'db_table': 'list_gainian',
            },
        ),
        migrations.CreateModel(
            name='hangye',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, verbose_name='行业名称')),
                ('code', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='行业代码')),
            ],
            options={
                'verbose_name_plural': '行业列表',
                'db_table': 'list_hangye',
            },
        ),
        migrations.CreateModel(
            name='stockinfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockname', models.CharField(max_length=10, verbose_name='股票名称')),
                ('stockcode', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='股票代码')),
                ('date', models.DateField(blank=True, db_index=True, verbose_name='交易日期')),
                ('tclose', models.FloatField(verbose_name='今收盘')),
                ('high', models.FloatField(verbose_name='最高价')),
                ('low', models.FloatField(verbose_name='最低价')),
                ('topen', models.FloatField(verbose_name='今开盘')),
                ('lclose', models.FloatField(verbose_name='前收盘')),
                ('chg', models.FloatField(verbose_name='涨跌额')),
                ('pchg', models.FloatField(verbose_name='涨跌幅')),
                ('tunover', models.FloatField(verbose_name='换手率')),
                ('voturnover', models.BigIntegerField(verbose_name='成交量')),
                ('vaturnover', models.BigIntegerField(verbose_name='成交金额')),
                ('tcap', models.BigIntegerField(verbose_name='总市值')),
                ('mcap', models.BigIntegerField(verbose_name='流通市值')),
            ],
            options={
                'verbose_name_plural': '交易数据',
                'db_table': 'stockinfo',
            },
        ),
        migrations.CreateModel(
            name='stocklist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stockid', models.CharField(max_length=10, unique=True, verbose_name='股票id')),
                ('stockname', models.CharField(max_length=10, verbose_name='股票名称')),
                ('stockcode', models.CharField(max_length=10, unique=True, verbose_name='股票代码')),
                ('hangye', models.CharField(max_length=10, verbose_name='行业')),
                ('gainian', models.CharField(max_length=10, verbose_name='概念')),
                ('diyu', models.CharField(max_length=10, verbose_name='地域')),
            ],
            options={
                'verbose_name_plural': '股票列表',
                'db_table': 'stocklist',
            },
        ),
    ]