from django import template

register = template.Library()

@register.filter
def split(value, arg):
    """分割字符串"""
    return value.split(arg)

@register.filter
def make_list(value):
    """将字符串转换为列表"""
    return list(value)

@register.filter
def mul(value, arg):
    """乘法运算"""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """除法运算"""
    try:
        return float(value) / float(arg) if float(arg) != 0 else 0
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """加法运算"""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0
