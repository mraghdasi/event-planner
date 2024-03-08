from django.contrib import admin

from users.models import *


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'is_lead')
    list_filter = ('is_lead',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = search_fields = ('title', 'is_active')
    list_filter = ('is_active',)
