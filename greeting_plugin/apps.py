# coding=utf-8

import logging

from django.apps import AppConfig
from django.conf import settings

from edx_django_utils.plugins import PluginSettings, PluginURLs
from openedx.core.djangoapps.plugins.constants import ProjectType, SettingsType

log = logging.getLogger(__name__)
IS_READY = False


class GreetingPluginAPIConfig(AppConfig):
    name = "greeting_plugin"
    label = "greeting_plugin"

    plugin_app = {

        PluginURLs.CONFIG: {
            ProjectType.LMS: {
                PluginURLs.NAMESPACE: name,
                PluginURLs.REGEX: "^greeting_plugin/api/",
                PluginURLs.RELATIVE_PATH: "urls",
            },
        },

        PluginSettings.CONFIG: {
            ProjectType.LMS: {
                SettingsType.PRODUCTION: {PluginSettings.RELATIVE_PATH: "settings.production"},
            },
        },
    }

    def ready(self):
        global IS_READY

        if IS_READY:
            return

        from .__about__ import __version__
        from .waffle import waffle_init

        log.info("{label} {version} is ready.".format(label=self.label, version=__version__))
        waffle_init()
        IS_READY = True
