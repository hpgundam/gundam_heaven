from django.contrib import admin

# Register your models here.
from gundam_heaven import models

admin.site.register(models.UserInfo)
admin.site.register(models.Article)
admin.site.register(models.Tag)
admin.site.register(models.Mark)
