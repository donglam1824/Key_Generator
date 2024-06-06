from django import template

register = template.Library()

@register.filter(name='truncate_key')    #Đăng ký một filter mới
def truncate_key(key, max_length = 50):
    if (len(key) > max_length):
        return key[:max_length] + "..."
    else:
        return key