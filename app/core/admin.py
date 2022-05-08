from django.contrib import admin

# change some of the variable of the imported class
from django.contrib.auth.admin import UserAdmin as BaseUA

from core import models

class UserAdmin(BaseUA):
    ordering = ['id']
    list_display = ['email', 'name']

admin.site.register(models.User, UserAdmin)