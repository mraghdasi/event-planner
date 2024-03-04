from django.contrib import admin

from account.models import *


@admin.register(User)
class ProfileAdmin(admin.ModelAdmin):
    list_display = search_fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'role')
    list_filter = ('role',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = search_fields = ('title', 'get_team_count', 'is_active')
    list_filter = ('is_active',)

    def get_team_count(self, obj):
        return obj.users.count()

    get_team_count.short_description = 'Members Count'
