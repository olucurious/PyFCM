import os
import threading

from pyfcm.baseapi import BaseAPI

from google.oauth2 import service_account
import google.auth.transport.requests

from pyfcm.errors import InvalidDataError


class BaseAPI(BaseAPI):
    FCM_END_POINT = "https://fcm.googleapis.com/v1/projects"

    def __init__(self, service_account_file_path: str, project_id: str, proxy_dict=None, env=None, json_encoder=None,
                 adapter=None):
        """
        Override existing init function to give ability to use v1 endpoints of Firebase Cloud Messaging API
        Attributes:
            service_account_file_path (str): path to service account JSON file
            project_id (str): project ID of Google account
            proxy_dict (dict): proxy settings dictionary, use proxy (keys: `http`, `https`)
            env (dict): environment settings dictionary, for example "app_engine"
            json_encoder (BaseJSONEncoder): JSON encoder
            adapter (BaseAdapter): adapter instance
        """
        self.service_account_file = service_account_file_path
        self.project_id = project_id
        self.FCM_END_POINT = self.FCM_END_POINT + f"/{self.project_id}/messages:send"
        self.FCM_REQ_PROXIES = None
        self.custom_adapter = adapter
        self.thread_local = threading.local()

        if proxy_dict and isinstance(proxy_dict, dict) and (('http' in proxy_dict) or ('https' in proxy_dict)):
            self.FCM_REQ_PROXIES = proxy_dict
            self.requests_session.proxies.update(proxy_dict)
        self.send_request_responses = []

        if env == 'app_engine':
            try:
                from requests_toolbelt.adapters import appengine
                appengine.monkeypatch()
            except ModuleNotFoundError:
                pass

        self.json_encoder = json_encoder

    def _get_access_token(self):
        """
            Generates access from refresh token that contains in the service_account_file.
            If token expires then new access token is generated.
            Returns:
                 str: Access token
        """
        # get OAuth 2.0 access token
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=['https://www.googleapis.com/auth/firebase.messaging'])
            request = google.auth.transport.requests.Request()
            credentials.refresh(request)
            return credentials.token
        except Exception as e:
            raise InvalidDataError(e)

    def request_headers(self):
        """
            Generates request headers including Content-Type and Authorization of Bearer token

            Returns:
                dict: request headers
        """
        return {
            "Content-Type": self.CONTENT_TYPE,
            "Authorization": "Bearer " + self._get_access_token(),
        }

    def parse_payload(self,
                      registration_ids=None,
                      topic_name=None,
                      message_body=None,
                      message_title=None,
                      message_icon=None,
                      sound=None,
                      condition=None,
                      collapse_key=None,
                      delay_while_idle=False,
                      time_to_live=None,
                      restricted_package_name=None,
                      low_priority=False,
                      dry_run=False,
                      data_message=None,
                      click_action=None,
                      badge=None,
                      color=None,
                      tag=None,
                      body_loc_key=None,
                      body_loc_args=None,
                      title_loc_key=None,
                      title_loc_args=None,
                      content_available=None,
                      remove_notification=False,
                      **extra_kwargs):

        """

        :rtype: json
        """
        fcm_payload = dict()
        if registration_ids:
            if len(registration_ids) > 1:
                fcm_payload['registration_ids'] = registration_ids
            else:
                fcm_payload['token'] = registration_ids[0]
        if condition:
            fcm_payload['condition'] = condition
        else:
            # In the `to` reference at: https://firebase.google.com/docs/cloud-messaging/http-server-ref#send-downstream
            # We have `Do not set this field (to) when sending to multiple topics`
            # Which is why it's in the `else` block since `condition` is used when multiple topics are being targeted
            if topic_name:
                fcm_payload['to'] = '/topics/%s' % topic_name
        # if low_priority:
        #     fcm_payload['priority'] = self.FCM_LOW_PRIORITY
        # else:
        #     fcm_payload['priority'] = self.FCM_HIGH_PRIORITY

        if delay_while_idle:
            fcm_payload['delay_while_idle'] = delay_while_idle
        if collapse_key:
            fcm_payload['collapse_key'] = collapse_key
        if time_to_live:
            if isinstance(time_to_live, int):
                fcm_payload['time_to_live'] = time_to_live
            else:
                raise InvalidDataError("Provided time_to_live is not an integer")
        if restricted_package_name:
            fcm_payload['restricted_package_name'] = restricted_package_name
        if dry_run:
            fcm_payload['dry_run'] = dry_run

        if data_message:
            if isinstance(data_message, dict):
                fcm_payload['message'] = data_message
            else:
                raise InvalidDataError("Provided data_message is in the wrong format")

        fcm_payload['notification'] = {}
        if message_icon:
            fcm_payload['notification']['icon'] = message_icon
        # If body is present, use it
        if message_body:
            fcm_payload['notification']['body'] = message_body
        # Else use body_loc_key and body_loc_args for body
        else:
            if body_loc_key:
                fcm_payload['notification']['body_loc_key'] = body_loc_key
            if body_loc_args:
                if isinstance(body_loc_args, list):
                    fcm_payload['notification']['body_loc_args'] = body_loc_args
                else:
                    raise InvalidDataError('body_loc_args should be an array')
        # If title is present, use it
        if message_title:
            fcm_payload['notification']['title'] = message_title
        # Else use title_loc_key and title_loc_args for title
        else:
            if title_loc_key:
                fcm_payload['notification']['title_loc_key'] = title_loc_key
            if title_loc_args:
                if isinstance(title_loc_args, list):
                    fcm_payload['notification']['title_loc_args'] = title_loc_args
                else:
                    raise InvalidDataError('title_loc_args should be an array')

        # This is needed for iOS when we are sending only custom data messages
        if content_available and isinstance(content_available, bool):
            fcm_payload['content_available'] = content_available

        if click_action:
            fcm_payload['notification']['click_action'] = click_action
        if badge:
            fcm_payload['notification']['badge'] = badge
        if color:
            fcm_payload['notification']['color'] = color
        if tag:
            fcm_payload['notification']['tag'] = tag
        # only add the 'sound' key if sound is not None
        # otherwise a default sound will play -- even with empty string args.
        if sound:
            fcm_payload['notification']['sound'] = sound

        if extra_kwargs:
            fcm_payload['notification'].update(extra_kwargs)

        # Do this if you only want to send a data message.
        if remove_notification:
            del fcm_payload['notification']

        return self.json_dumps({"message": fcm_payload})
