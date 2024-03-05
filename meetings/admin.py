from django.contrib import admin

from meetings.models import *


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = search_fields = ('title', 'is_active')
    list_filter = ('is_active',)


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = search_fields = ('title', 'get_team_title', 'get_room_title', 'start_date', 'end_date')
    list_filter = ('team', 'room', 'start_date')

    def get_team_title(self, obj):
        return obj.team.title

    def get_room_title(self, obj):
        return obj.room.title

    get_team_title.short_description = 'Team'
    get_room_title.short_description = 'Room'


@admin.register(CommentRoom)
class CommentRoomAdmin(admin.ModelAdmin):
    list_display = search_fields = ('get_username', 'get_room_title', 'body', 'rate')
    list_filter = ('user', 'room')

    def get_username(self, obj):
        return obj.user.username

    def get_room_title(self, obj):
        return obj.room.title

    get_username.short_description = 'User'
    get_room_title.short_description = 'Room'
