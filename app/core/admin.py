from django.contrib import admin

# Changing some of the variable of the imported class
from django.contrib.auth.admin import UserAdmin as BaseUA
# Converting strings in python to human-readable content
from django.utils.translation import gettext
from core import models

class UserAdmin(BaseUA):
    ordering = ['id']
    list_display = ['email', 'name']
    # To group fields into different sections
    """
    e.g. for 1 fieldset:
    (section_name, {
        ("fields":(field1, field2, etc...)
    })
   """ 
    fieldsets = (
        (None, {
            "fields": (
                'email', 'password'                
            )
        }),
        (gettext('Personal Info'), {'fields':('name',)}),
        (
            gettext('Permissions'),
            {
                'fields':(
                    'is_staff', 'is_superuser'
                )
            }
        ),
        (gettext('Important Dates'), {'fields':('last_login', )})
    )
    
admin.site.register(models.User, UserAdmin)