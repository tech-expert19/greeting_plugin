"""
written by:     Raza Fayyaz

date:           August-2022

usage:          register the UserGreeting model in LMS Django Admin
"""
from django.contrib import admin
from greeting_plugin.models import UserGreetings


class UserGreetingsAdmin(admin.ModelAdmin):
    list_display = ['message', 'date_added']
    list_filter = [
        'message'
    ]
    search_fields = [
        'message'
    ]


admin.site.register(UserGreetings, UserGreetingsAdmin)
