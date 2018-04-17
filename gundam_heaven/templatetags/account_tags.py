from django import template

register = template.Library()

@register.filter(name='is_fan_of')
def is_fan_of(follower, followee):
    return follower in [ item.follower for item in followee.followers.all()]
