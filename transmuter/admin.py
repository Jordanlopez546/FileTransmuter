from django.contrib import admin
from .models import *
# Register your models here.

class UserProfilePanel(admin.ModelAdmin):
  list_display = ['user', 'address', 'phone_number']


admin.site.register(UserProfile, UserProfilePanel)