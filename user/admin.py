from django.contrib import admin


# Register your models here.
from .models import user_stock


class user_stockAdmin(admin.ModelAdmin):
    list_display = ( 'userid', 'username', 'stockname','stockcode', )
    list_per_page = 12
    list_filter = ('username',)
    search_fields = ('username','stockname','stockcode',)
    # 更新按钮

admin.site.register(user_stock, user_stockAdmin)
