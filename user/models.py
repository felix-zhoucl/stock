from django.db import models


# Create your models here.
# class myUser(models.Model):
#     username = models.CharField(max_length=20, unique=True, verbose_name='用户名称')
#     password = models.CharField(max_length=40, verbose_name='用户密码')
#     email = models.EmailField(unique=True,verbose_name='用户邮箱')
#     is_active = models.BooleanField(default=True, verbose_name='激活状态')
#     class Meta:
#        db_table = 'myuser'

class user_stock(models.Model):
    userid = models.IntegerField(verbose_name='用户ID')
    username = models.CharField(max_length=20, verbose_name='用户名称')
    stockcode = models.CharField(max_length=10, verbose_name='股票代码')
    stockname = models.CharField(max_length=10, verbose_name='股票名称')
    class Meta:
        db_table = 'user_stock'
        verbose_name_plural = '收藏管理'