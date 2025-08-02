from django.contrib import admin

# Register your models here.

from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.


class UserModelAdmin(UserAdmin):
    list_display = ['id','mobile','credit','money']


admin.site.register(User, UserModelAdmin)