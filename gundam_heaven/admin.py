from django.contrib import admin

# Register your models here.
from gundam_heaven.models import UserInfo, Article

admin.site.register(UserInfo)
admin.site.register(Article)
