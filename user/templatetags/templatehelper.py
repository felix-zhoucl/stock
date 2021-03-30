from django import template
register = template.Library()
@register.filter
def div(value, div):
    '''
    分转化为元，保留两位小数
    :param value:
    :param div:
    :return:
    '''
    return round((value / div), 2)