# coding=utf-8
import os
import logging

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

from openedx.core.djangoapps.api_admin.models import (
    ApiAccessConfig,
    ApiAccessRequest,
)
from oauth2_provider.models import Application

from ...waffle import waffle_init

User = get_user_model()
logger = logging.getLogger(__name__)

PLUGIN_API_USER_NAME = 'raza_admin'
PLUGIN_API_USER_EMAIL = 'raza.fayyaz.rf@gmail.com'
PLUGIN_API_USER_PASSWORD = 'AzaR!1234'
OPENEDX_CLIENT_ID = 'HA5yo-bNURv-O1RGi-Cf1by'
OPENEDX_CLIENT_SECRET = 'wdZVJ-gdo2i-tfCGK-v0Fvn-IPbyl-xM3sW-lI85G'
OPENEDX_COMPLETE_DOMAIN_NAME = 'local.overhang.io'


class Command(BaseCommand):
    help = "Verifies initialization records for all Django models in this plugin"

    def handle(self, *args, **options):
        waffle_init()

        if not all(
            [
                PLUGIN_API_USER_EMAIL,
                PLUGIN_API_USER_NAME,
                PLUGIN_API_USER_PASSWORD,
                OPENEDX_COMPLETE_DOMAIN_NAME,
            ]
        ):
            raise Exception("Missing required parameters")
        logger.info("Assert API user")
        user, created = User.objects.get_or_create(
            username=PLUGIN_API_USER_NAME, defaults={"email": PLUGIN_API_USER_EMAIL}
        )
        user.set_password(PLUGIN_API_USER_PASSWORD)
        user.save()

        logger.info("Assert API access")
        self.api_access()

        logger.info("Retrieve the client id and secret via the Admin")

    def api_access(self):
        site, _ = Site.objects.get_or_create(domain=OPENEDX_COMPLETE_DOMAIN_NAME)
        config = ApiAccessConfig.objects.filter(enabled=True).first()
        if not config:
            config = ApiAccessConfig(enabled=True)
            config.save()
        user = User.objects.get(username=PLUGIN_API_USER_NAME)
        try:
            access = ApiAccessRequest.objects.get(user=user)
        except ApiAccessRequest.DoesNotExist:
            access = ApiAccessRequest()
        access.user = user
        access.status = ApiAccessRequest.APPROVED
        access.website = OPENEDX_COMPLETE_DOMAIN_NAME
        access.site = site
        access.reason = "Created from bootstrap script"
        access.save()
        application, _ = Application.objects.get_or_create(
            user=user,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            client_type=Application.CLIENT_CONFIDENTIAL,
        )
        if OPENEDX_CLIENT_ID and OPENEDX_CLIENT_SECRET:
            application.client_id = OPENEDX_CLIENT_ID
            application.client_secret = OPENEDX_CLIENT_SECRET
        application.save()
