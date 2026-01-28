from django import template

register = template.Library()

@register.filter
def modulo(num:int, val:int) -> int:
    """
    returns num modulo val
    
    :param num: Integer number
    :param val: Integer value to modulo by
    """
    return num % val