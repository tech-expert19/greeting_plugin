import logging
import requests
import json
from datetime import datetime
import os

from openedx.core.lib.api.view_utils import view_auth_classes
from oauth2_provider.models import AccessToken

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse

from greeting_plugin.models import UserGreetings


log = logging.getLogger(__name__)


class ResponseMethod(Response):
    def __init__(self, data=None, success=False, http_status=None, content_type=None):
        _status = http_status or status.HTTP_200_OK
        data = data or {}
        reply = {"response": {"success": success}}
        reply["response"].update(data)
        super().__init__(data=reply, status=_status, content_type=content_type)


@view_auth_classes(is_authenticated=True)
class GreetingsAPIView(APIView):
    def post(self, request):
        message = request.data.get("message")
        if message:
            log.info("GreetingsAPIView() received message of {message} from user {user_name}".format(message=message, user_name=request.user.username))
            greeting = UserGreetings.objects.create(user=request.user, message=message)
            greeting.save()
            if message.lower() == "hello":
                self.send_goodbye_greeting()

            return ResponseMethod(success=True, content_type="application/json")

        return ResponseMethod(success=False, content_type="application/json")

    def send_goodbye_greeting(self):
        goodbye_endpoint = self.request.build_absolute_uri(reverse("greeting_plugin:openedx_plugin_api_greeting_users"))

        # Try to find the token from the user which have sent the request
        acess_token = AccessToken.objects.filter(user=self.request.user, expires__gt=datetime.now()).first()
        if acess_token:
            headers = {
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {acess_token.token}"
                    }

            payload = json.dumps({
                "message": "goodbye"
            })
            requests.post(goodbye_endpoint, data=payload, headers=headers)

        else:
            # if access token is not available or expired create a new one using client-id and client-secret
            access_token = self.generate_token()
            if access_token:
                headers = {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {acess_token}"
                        }
                payload = json.dumps({
                    "message": "goodbye"
                })
                requests.post(goodbye_endpoint, data=payload, headers=headers)
            else:
                log.info("no access token found")

    def generate_token(self):
        client_id = 'HA5yo-bNURv-O1RGi-Cf1by'
        client_secret = 'wdZVJ-gdo2i-tfCGK-v0Fvn-IPbyl-xM3sW-lI85G'
        token_url = self.request.build_absolute_uri('/oauth2/access_token')

        # Define the payload to request the access token
        token_payload = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }

        # Make a POST request to the token endpoint to get the access token
        token_response = requests.post(token_url, data=token_payload)
        if token_response.status_code == 200:
            access_token = token_response.json().get('access_token', '')
            return access_token
        return ''
