from django.contrib import admin

from .models import User, UserCode

admin.site.register(User)
admin.site.register(UserCode)
