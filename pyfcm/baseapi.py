import json
import os
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


from .errors import AuthenticationError, InvalidDataError, FCMError, FCMServerError, FCMNotRegisteredError


class BaseAPI(object):
    """
    Base class for the pyfcm API wrapper for FCM

    Attributes:
        api_key (str): Firebase API key
        proxy_dict (dict): use proxy (keys: `http`, `https`)
        env (str): for example "app_engine"
        json_encoder
        adapter: requests.adapters.HTTPAdapter()
    """

    CONTENT_TYPE = "application/json"
    FCM_END_POINT = "https://fcm.googleapis.com/fcm/send"
    INFO_END_POINT = 'https://iid.googleapis.com/iid/info/'
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

    # Number of times to retry calls to info endpoint
    INFO_RETRIES = 3

    def __init__(self, api_key=None, proxy_dict=None, env=None, json_encoder=None, adapter=None):
        if api_key:
            self._FCM_API_KEY = api_key
        elif os.getenv('FCM_API_KEY', None):
            self._FCM_API_KEY = os.getenv('FCM_API_KEY', None)
        else:
            raise AuthenticationError("Please provide the api_key in the google-services.json file")

        self.FCM_REQ_PROXIES = None
        self.requests_session = requests.Session()
        retries = Retry(backoff_factor=1, status_forcelist=[502, 503],
                        allowed_methods=(Retry.DEFAULT_ALLOWED_METHODS | frozenset(['POST'])))
        self.requests_session.mount('http://', adapter or HTTPAdapter(max_retries=retries))
        self.requests_session.mount('https://', adapter or HTTPAdapter(max_retries=retries))
        self.requests_session.headers.update(self.request_headers())
        self.requests_session.mount(self.INFO_END_POINT, HTTPAdapter(max_retries=self.INFO_RETRIES))

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

    def request_headers(self):
        """
        Generates request headers including Content-Type and Authorization

        Returns:
            dict: request headers
        """
        return {
            "Content-Type": self.CONTENT_TYPE,
            "Authorization": "key=" + self._FCM_API_KEY,
        }

    def registration_id_chunks(self, registration_ids):
        """
        Splits registration ids in several lists of max 1000 registration ids per list

        Args:
            registration_ids (list): FCM device registration ID

        Yields:
            generator: list including lists with registration ids
        """
        try:
            xrange
        except NameError:
            xrange = range

        # Yield successive 1000-sized (max fcm recipients per request) chunks from registration_ids
        for i in xrange(0, len(registration_ids), self.FCM_MAX_RECIPIENTS):
            yield registration_ids[i:i + self.FCM_MAX_RECIPIENTS]

    def json_dumps(self, data):
        """
        Standardized json.dumps function with separators and sorted keys set

        Args:
            data (dict or list): data to be dumped

        Returns:
            string: json
        """
        return json.dumps(
            data,
            separators=(',', ':'),
            sort_keys=True,
            cls=self.json_encoder,
            ensure_ascii=False
        ).encode('utf8')

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
                      android_channel_id=None,
                      extra_notification_kwargs={},
                      **extra_kwargs):
        """
        Parses parameters of FCMNotification's methods to FCM nested json

        Args:
            registration_ids (list, optional): FCM device registration IDs
            topic_name (str, optional): Name of the topic to deliver messages to
            message_body (str, optional): Message string to display in the notification tray
            message_title (str, optional): Message title to display in the notification tray
            message_icon (str, optional): Icon that apperas next to the notification
            sound (str, optional): The sound file name to play. Specify "Default" for device default sound.
            condition (str, optiona): Topic condition to deliver messages to
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to `None`.
            delay_while_idle (bool, optional): deprecated
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to `None`
                which uses the FCM default of 4 weeks.
            restricted_package_name (str, optional): Name of package
            low_priority (bool, optional): Whether to send notification with
                the low priority flag. Defaults to `False`.
            dry_run (bool, optional): If `True` no message will be sent but request will be tested.
            data_message (dict, optional): Custom key-value pairs
            click_action (str, optional): Action associated with a user click on the notification
            badge (str, optional): Badge of notification
            color (str, optional): Color of the icon
            tag (str, optional): Group notification by tag
            body_loc_key (str, optional): Indicates the key to the body string for localization
            body_loc_args (list, optional): Indicates the string value to replace format
                specifiers in body string for localization
            title_loc_key (str, optional): Indicates the key to the title string for localization
            title_loc_args (list, optional): Indicates the string value to replace format
                specifiers in title string for localization
            content_available (bool, optional): Inactive client app is awoken
            remove_notification (bool, optional): Only send a data message
            android_channel_id (str, optional): Starting in Android 8.0 (API level 26),
                all notifications must be assigned to a channel. For each channel, you can set the
                visual and auditory behavior that is applied to all notifications in that channel.
                Then, users can change these settings and decide which notification channels from
                your app should be intrusive or visible at all.
            extra_notification_kwargs (dict, optional): More notification keyword arguments
            **extra_kwargs (dict, optional): More keyword arguments

        Returns:
            string: json

        Raises:
            InvalidDataError: parameters do have the wrong type or format
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
                fcm_payload['to'] = '/topics/%s' % topic_name
        # Revert to legacy API compatible priority
        if low_priority:
            fcm_payload['priority'] = self.FCM_LOW_PRIORITY
        else:
            fcm_payload['priority'] = self.FCM_HIGH_PRIORITY

        if delay_while_idle:
            fcm_payload['delay_while_idle'] = delay_while_idle
        if collapse_key:
            fcm_payload['collapse_key'] = collapse_key
        if time_to_live is not None:
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
                fcm_payload['data'] = data_message
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

        if android_channel_id:
            fcm_payload['notification']['android_channel_id'] = android_channel_id

        # This is needed for iOS when we are sending only custom data messages
        if content_available and isinstance(content_available, bool):
            fcm_payload['content_available'] = content_available

        if click_action:
            fcm_payload['notification']['click_action'] = click_action
        if isinstance(badge, int) and badge >= 0:
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
            fcm_payload.update(extra_kwargs)

        if extra_notification_kwargs:
            fcm_payload['notification'].update(extra_notification_kwargs)

        # Do this if you only want to send a data message.
        if remove_notification:
            del fcm_payload['notification']

        return self.json_dumps(fcm_payload)

    def do_request(self, payload, timeout):
        response = self.requests_session.post(self.FCM_END_POINT, data=payload, timeout=timeout)
        if 'Retry-After' in response.headers and int(response.headers['Retry-After']) > 0:
            sleep_time = int(response.headers['Retry-After'])
            time.sleep(sleep_time)
            return self.do_request(payload, timeout)
        return response

    def send_request(self, payloads=None, timeout=None):
        self.send_request_responses = []
        for payload in payloads:
            response = self.do_request(payload, timeout)
            self.send_request_responses.append(response)

    def registration_info_request(self, registration_id):
        """
        Makes a request for registration info and returns the response object

        Args:
            registration_id: id to be checked

        Returns:
            response of registration info request
        """
        return self.requests_session.get(
            self.INFO_END_POINT + registration_id,
            params={'details': 'true'}
        )

    def clean_registration_ids(self, registration_ids=[]):
        """
        Checks registration ids and excludes inactive ids

        Args:
            registration_ids (list, optional): list of ids to be cleaned

        Returns:
            list: cleaned registration ids
        """
        valid_registration_ids = []
        for registration_id in registration_ids:
            details = self.registration_info_request(registration_id)
            if details.status_code == 200:
                valid_registration_ids.append(registration_id)
        return valid_registration_ids

    def get_registration_id_info(self, registration_id):
        """
        Returns details related to a registration id if it exists otherwise return None

        Args:
            registration_id: id to be checked

        Returns:
            dict: info about registration id
            None: if id doesn't exist
        """
        response = self.registration_info_request(registration_id)
        if response.status_code == 200:
            return response.json()
        return None

    def subscribe_registration_ids_to_topic(self, registration_ids, topic_name):
        """
        Subscribes a list of registration ids to a topic

        Args:
            registration_ids (list): ids to be subscribed
            topic_name (str): name of topic

        Returns:
            True: if operation succeeded

        Raises:
            InvalidDataError: data sent to server was incorrectly formatted
            FCMError: an error occured on the server
        """
        url = 'https://iid.googleapis.com/iid/v1:batchAdd'
        payload = {
            'to': '/topics/' + topic_name,
            'registration_tokens': registration_ids,
        }
        response = self.requests_session.post(url, json=payload)
        if response.status_code == 200:
            return True
        elif response.status_code == 400:
            error = response.json()
            raise InvalidDataError(error['error'])
        else:
            raise FCMError()

    def unsubscribe_registration_ids_from_topic(self, registration_ids, topic_name):
        """
        Unsubscribes a list of registration ids from a topic

        Args:
            registration_ids (list): ids to be unsubscribed
            topic_name (str): name of topic

        Returns:
            True: if operation succeeded

        Raises:
            InvalidDataError: data sent to server was incorrectly formatted
            FCMError: an error occured on the server
        """
        url = "https://iid.googleapis.com/iid/v1:batchRemove"
        payload = {
            'to': '/topics/' + topic_name,
            'registration_tokens': registration_ids,
        }
        response = self.requests_session.post(url, json=payload)
        if response.status_code == 200:
            return True
        elif response.status_code == 400:
            error = response.json()
            raise InvalidDataError(error['error'])
        else:
            raise FCMError()

    def parse_responses(self):
        """
        Parses the json response sent back by the server and tries to get out the important return variables

        Returns:
            dict: multicast_ids (list), success (int), failure (int), canonical_ids (int),
                results (list) and optional topic_message_id (str but None by default)

        Raises:
            FCMServerError: FCM is temporary not available
            AuthenticationError: error authenticating the sender account
            InvalidDataError: data passed to FCM was incorrecly structured
        """
        response_dict = {
            'multicast_ids': [],
            'success': 0,
            'failure': 0,
            'canonical_ids': 0,
            'results': [],
            'topic_message_id': None
        }

        for response in self.send_request_responses:
            if response.status_code == 200:
                if 'content-length' in response.headers and int(response.headers['content-length']) <= 0:
                    raise FCMServerError("FCM server connection error, the response is empty")
                else:
                    parsed_response = response.json()

                    multicast_id = parsed_response.get('multicast_id', None)
                    success = parsed_response.get('success', 0)
                    failure = parsed_response.get('failure', 0)
                    canonical_ids = parsed_response.get('canonical_ids', 0)
                    results = parsed_response.get('results', [])
                    message_id = parsed_response.get('message_id', None)  # for topic messages
                    if message_id:
                        success = 1
                    if multicast_id:
                        response_dict['multicast_ids'].append(multicast_id)
                    response_dict['success'] += success
                    response_dict['failure'] += failure
                    response_dict['canonical_ids'] += canonical_ids
                    response_dict['results'].extend(results)
                    response_dict['topic_message_id'] = message_id

            elif response.status_code == 401:
                raise AuthenticationError("There was an error authenticating the sender account")
            elif response.status_code == 400:
                raise InvalidDataError(response.text)
            elif response.status_code == 404:
                raise FCMNotRegisteredError("Token not registered")
            else:
                raise FCMServerError("FCM server is temporarily unavailable")
        return response_dict

    def send_async_request(self,params_list,timeout):

        import asyncio
        from .async_fcm import fetch_tasks

        payloads = [ self.parse_payload(**params) for params in params_list ]
        responses = asyncio.new_event_loop().run_until_complete(fetch_tasks(end_point=self.FCM_END_POINT,headers=self.request_headers(),payloads=payloads,timeout=timeout))

        return responses


