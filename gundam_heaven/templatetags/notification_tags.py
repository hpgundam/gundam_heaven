from django import template

register = template.Library()

@register.filter(name='get_unread_noti_amt')
def get_unread_noti_amt(user):
    return user.notifications.filter(has_read=False).count()


