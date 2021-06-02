from django.contrib import admin
from .models import Task,UserPic,UserInfo

# Register your models here.
admin.site.register(Task)
admin.site.register(UserPic)
admin.site.register(UserInfo)