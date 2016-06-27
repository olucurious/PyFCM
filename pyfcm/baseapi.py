import os
import requests
import json

from .errors import *
import logging


class BaseAPI(object):
    """
    Base class for the pyfcm API wrapper for FCM
    """

    CONTENT_TYPE = "application/json"
    FCM_END_POINT = "https://fcm.googleapis.com/fcm/send"
    # FCM only allows up to 1000 reg ids per bulk message.
    FCM_MAX_RECIPIENTS = 1000

    #: Indicates that the push message should be sent with low priority. Low
    #: priority optimizes the client app's battery consumption, and should be used
    #: unless immediate delivery is required. For messages with low priority, the
    #: app may receive the message with unspecified delay.
    FCM_LOW_PRIORITY = 'normal'

    #: Indicates that the push message should be sent with a high priority. When a
    #: message is sent with high priority, it is sent immediately, and the app can
    #: wake a sleeping device and open a network connection to your server.
    FCM_HIGH_PRIORITY = 'high'

    def __init__(self, api_key=None):
        if api_key:
            self._FCM_API_KEY = api_key
        elif os.getenv('FCM_API_KEY', None):
            self._FCM_API_KEY = os.getenv('FCM_API_KEY', None)
        else:
            raise AuthenticationError("Please provide the api_key in the google-services.json file")

    def request_headers(self):
        return {
            "Content-Type": self.CONTENT_TYPE,
            "Authorization": "key=" + self._FCM_API_KEY,
        }

    def parse_response(self, response):
        """
        Parses the json response sent back by the
        server and tries to get out the important return variables

        Returns a python dict of multicast_id(long), success(int), failure(int), canonical_ids(int), results(list)
        """
        if 'content-length' in response.headers and int(response.headers['content-length']) <= 0:
            return {}
        parsed_response = response.json()

        multicast_id = parsed_response.get('multicast_id', None)
        success = parsed_response.get('success', 0)
        failure = parsed_response.get('failure', 0)
        canonical_ids = parsed_response.get('canonical_ids', 0)
        results = parsed_response.get('results', [])
        message_id = parsed_response.get('message_id', None)  # for topic messages
        if message_id:
            success = 1

        return {'multicast_id': multicast_id,
                'success': success,
                'failure': failure,
                'canonical_ids': canonical_ids,
                'results': results}

    def registration_id_chunks(self, registration_ids):
        try:
            xrange
        except NameError:
            xrange = range
        """Yield successive 1000-sized (max fcm recipients per request) chunks from registration_ids."""
        for i in xrange(0, len(registration_ids), self.FCM_MAX_RECIPIENTS):
            yield registration_ids[i:i + self.FCM_MAX_RECIPIENTS]

    def json_dumps(self, data):
        """Standardized json.dumps function with separators and sorted keys set."""
        return (json.dumps(data, separators=(',', ':'), sort_keys=True)
                .encode('utf8'))

    def parse_payload(self,
                      registration_ids=None,
                      topic_name=None,
                      message_body=None,
                      message_title=None,
                      message_icon=None,
                      condition=None,
                      collapse_key=None,
                      delay_while_idle=False,
                      time_to_live=None,
                      restricted_package_name=None,
                      low_priority=False,
                      dry_run=False,
                      data_message=None):

        """

        :rtype: json
        """
        fcm_payload = dict()
        if registration_ids:
            if len(registration_ids) > 1:
                fcm_payload['registration_ids'] = registration_ids
            else:
                fcm_payload['to'] = registration_ids[0]
        if condition:
            fcm_payload['condition'] = condition
        else:
            # In the `to` reference at: https://firebase.google.com/docs/cloud-messaging/http-server-ref#send-downstream
            # We have `Do not set this field (to) when sending to multiple topics`
            # Which is why it's in the `else` block since `condition` is used when multiple topics are being targeted
            if topic_name:
                fcm_payload['to'] = '/topics/%s' % (topic_name)
        if low_priority:
            fcm_payload['priority'] = self.FCM_LOW_PRIORITY
        else:
            fcm_payload['priority'] = self.FCM_HIGH_PRIORITY

        if delay_while_idle:
            fcm_payload['delay_while_idle'] = delay_while_idle
        if collapse_key:
            fcm_payload['collapse_key'] = collapse_key
        if time_to_live and isinstance(time_to_live, int):
            fcm_payload['time_to_live'] = time_to_live
        if restricted_package_name:
            fcm_payload['restricted_package_name'] = restricted_package_name
        if dry_run:
            fcm_payload['dry_run'] = dry_run

        if data_message and isinstance(data_message, dict):
            fcm_payload['data'] = data_message
        if message_body:
            fcm_payload['notification'] = {
                'body': message_body,
                'title': message_title,
                'icon': message_icon
            }
        else:
            # This is needed for iOS when we are sending only custom data messages
            fcm_payload['content_available'] = True

        return self.json_dumps(fcm_payload)

    def send_request(self, payloads=None):

        for payload in payloads:
            response = requests.post(self.FCM_END_POINT, headers=self.request_headers(), data=payload, verify=True)

            if response.status_code == 200:
                return self.parse_response(response)
            elif response.status_code == 401:
                raise AuthenticationError("There was an error authenticating the sender account")
            elif response.status_code == 400:
                raise InternalPackageError("Please create a new github issue describing what you're doing")
            else:
                raise FCMServerError("FCM server is temporarily unavailable")
