from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class UserModelAdmin(UserAdmin):
    list_display = ['id','mobile','email','nickname','credit','money',]

    # 默认排序字段
    ordering = ["id"]


admin.site.register(User, UserModelAdmin)