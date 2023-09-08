from django.urls import path

from greeting_plugin.waffle import (
    waffle_switches,
    API_USERS,
)
from greeting_plugin import views

urlpatterns = []

if waffle_switches[API_USERS]:
    urlpatterns += [
        path("", views.GreetingsAPIView.as_view(), name="openedx_plugin_api_greeting_users"),
    ]
