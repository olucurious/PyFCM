# from __future__ import annotations

from functools import cached_property
import json
import time
import threading
from datetime import datetime, timedelta, timezone

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from google.oauth2 import service_account
from google.auth.credentials import Credentials
import google.auth.transport.requests

from pyfcm.errors import (
    AuthenticationError,
    InvalidDataError,
    FCMSenderIdMismatchError,
    FCMServerError,
    FCMNotRegisteredError,
)

# Migration to v1 - https://firebase.google.com/docs/cloud-messaging/migrate-v1


class BaseAPI(object):
    FCM_END_POINT_BASE = "https://fcm.googleapis.com/v1/projects"

    def __init__(
        self,
        service_account_file: str | None = None,
        project_id: str | None = None,
        credentials: Credentials | None = None,
        proxy_dict: dict | None = None,
        env: str | None = None,
        json_encoder=None,
        adapter=None,
    ):
        """
        Override existing init function to give ability to use v1 endpoints of Firebase Cloud Messaging API
        Attributes:
            service_account_file (str): path to service account JSON file
            project_id (str): project ID of Google account
            credentials (Credentials): Google auth credentials instance, such as ADC, service account one
            proxy_dict (dict): proxy settings dictionary, use proxy (keys: `http`, `https`)
            env (dict): environment settings dictionary, for example "app_engine"
            json_encoder (BaseJSONEncoder): JSON encoder
            adapter (BaseAdapter): adapter instance
        """
        if not (service_account_file or credentials):
            raise AuthenticationError(
                "Please provide a service account file path or credentials in the constructor"
            )

        self._service_account_file = service_account_file
        self._project_id = project_id
        self._provided_credentials = credentials
        self.custom_adapter = adapter
        self.thread_local = threading.local()

        # Shared token management across threads
        self._shared_token = None
        self._token_lock = threading.RLock()

        if (
            proxy_dict
            and isinstance(proxy_dict, dict)
            and (("http" in proxy_dict) or ("https" in proxy_dict))
        ):
            self.requests_session.proxies.update(proxy_dict)

        if env == "app_engine":
            try:
                from requests_toolbelt.adapters import appengine

                appengine.monkeypatch()
            except ModuleNotFoundError:
                pass

        self.json_encoder = json_encoder

    @cached_property
    def _credentials(self) -> Credentials:
        if self._provided_credentials is not None:
            return self._provided_credentials

        credentials = service_account.Credentials.from_service_account_file(
            self._service_account_file,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"],
        )
        # Service account credentials has project_id (others are not)
        self._project_id = credentials.project_id or self._project_id
        self._service_account_file = None
        return credentials

    @cached_property
    def fcm_end_point(self) -> str:
        if self._provided_credentials is None:
            # read credentails to resolve project_id if needed
            _ = self._credentials
        if self._project_id is None:
            raise RuntimeError("Please provide a project_id either explicitly or through Google credentials.")
        return self.FCM_END_POINT_BASE + f"/{self._project_id}/messages:send"

    @property
    def requests_session(self):
        if getattr(self.thread_local, "requests_session", None) is None:
            retries = Retry(
                backoff_factor=1,
                status_forcelist=[502, 503],
                allowed_methods=(Retry.DEFAULT_ALLOWED_METHODS | frozenset(["POST"])),
            )
            adapter = self.custom_adapter or HTTPAdapter(max_retries=retries)
            self.thread_local.requests_session = requests.Session()
            self.thread_local.requests_session.mount("http://", adapter)
            self.thread_local.requests_session.mount("https://", adapter)

        # Always update headers with current shared token
        self.thread_local.requests_session.headers.update(self.request_headers())
        return self.thread_local.requests_session

    def send_request(self, payload=None, timeout=None):
        response = self.requests_session.post(
            self.fcm_end_point, data=payload, timeout=timeout
        )
        if (
            "Retry-After" in response.headers
            and int(response.headers["Retry-After"]) > 0
        ):
            sleep_time = int(response.headers["Retry-After"])
            time.sleep(sleep_time)
            return self.send_request(payload, timeout)

        if self._is_access_token_expired(response):
            # Clear shared token and refresh credentials
            with self._token_lock:
                self._shared_token = None
                if self._credentials:
                    try:
                        request = google.auth.transport.requests.Request()
                        self._credentials.refresh(request)
                    except Exception:
                        # If refresh fails, let the next request handle it
                        pass
            return self.send_request(payload, timeout)

        return response

    def send_async_request(self, params_list, timeout):
        import asyncio
        from .async_fcm import fetch_tasks

        payloads = [self.parse_payload(**params) for params in params_list]
        responses = asyncio.new_event_loop().run_until_complete(
            fetch_tasks(
                end_point=self.fcm_end_point,
                headers=self.request_headers(),
                payloads=payloads,
                timeout=timeout,
            )
        )

        return responses

    def _is_access_token_expired(self, response):
        """
        Check if the response indicates an expired access token

        Args:
            response: HTTP response object

        Returns:
            bool: True if access token is expired, False otherwise
        """
        if response.status_code != 401:
            return False

        try:
            error_response = response.json()
            error_details = error_response.get("error", {}).get("details", [])
            for detail in error_details:
                if detail.get("reason") == "ACCESS_TOKEN_EXPIRED":
                    return True
        except (ValueError, AttributeError):
            pass

        return False

    def _is_token_valid(self) -> bool:
        """
        Enhanced token validity check with fallback mechanisms.
        Combines expired property check with time-based validation.

        Returns:
            bool: True if token is valid, False otherwise
        """
        if not self._shared_token:
            return False

        if self._credentials.expired:
            return False

        # Fallback check: time-based validation with 5-minute buffer
        # This accounts for the 4-minute early expiration issue
        if (hasattr(self._credentials, 'expiry') and
                self._credentials.expiry and
                self._credentials.expiry <= datetime.now(timezone.utc) + timedelta(minutes=5)):
            return False

        return True

    def _get_access_token(self) -> str:
        """
        Thread-safe access token management with shared token across threads.
        Uses double-checked locking pattern for performance with enhanced validation.
        Returns:
             str: Access token
        """
        # First check without lock (performance optimization)
        if self._is_token_valid():
            return self._shared_token

        # Acquire lock and check again (double-checked locking)
        with self._token_lock:
            if self._is_token_valid():
                return self._shared_token

            try:
                request = google.auth.transport.requests.Request()
                self._credentials.refresh(request)
                self._shared_token = self._credentials.token
                return self._shared_token
            except Exception as e:
                raise InvalidDataError(e)

    def request_headers(self):
        """
        Generates request headers including Content-Type and Authorization of Bearer token

        Returns:
            dict: request headers
        """
        return {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + self._get_access_token(),
        }

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
            separators=(",", ":"),
            sort_keys=True,
            cls=self.json_encoder,
            ensure_ascii=False,
        ).encode("utf8")

    def parse_response(self, response):
        """
        Parses the json response sent back by the server and tries to get out the important return variables

        Returns:
            dict: name (str) - The identifier of the message sent, in the format of projects/*/messages/{message_id}

        Raises:
            FCMServerError: FCM is temporary not available
            AuthenticationError: error authenticating the sender account
            InvalidDataError: data passed to FCM was incorrecly structured
            FCMSenderIdMismatchError: the authenticated sender is different from the sender registered to the token
            FCMNotRegisteredError: device token is missing, not registered, or invalid
        """
        if response.status_code == 200:
            if (
                "content-length" in response.headers
                and int(response.headers["content-length"]) <= 0
            ):
                raise FCMServerError(
                    "FCM server connection error, the response is empty"
                )
            else:
                return response.json()

        elif response.status_code == 401:
            raise AuthenticationError(
                "There was an error authenticating the sender account"
            )
        elif response.status_code == 400:
            raise InvalidDataError(response.text)
        elif response.status_code == 403:
            raise FCMSenderIdMismatchError(
                "The authenticated sender ID is different from the sender ID for the registration token."
            )
        elif response.status_code == 404:
            raise FCMNotRegisteredError("Token not registered")
        else:
            raise FCMServerError(
                f"FCM server error: Unexpected status code {response.status_code}. "
                "The server might be temporarily unavailable."
            )

    def parse_payload(  # noqa: C901
        self,
        fcm_token=None,
        notification_title=None,
        notification_body=None,
        notification_image=None,
        data_payload=None,
        topic_name=None,
        topic_condition=None,
        android_config=None,
        apns_config=None,
        webpush_config=None,
        fcm_options=None,
        dry_run=False,
    ):
        """

        :rtype: json
        """
        fcm_payload = dict()

        if fcm_token:
            fcm_payload["token"] = fcm_token

        if topic_name:
            fcm_payload["topic"] = topic_name
        if topic_condition:
            fcm_payload["condition"] = topic_condition

        if data_payload:
            if isinstance(data_payload, dict):
                fcm_payload["data"] = data_payload
            else:
                raise InvalidDataError("Provided data_payload is in the wrong format")

        if android_config:
            if isinstance(android_config, dict):
                fcm_payload["android"] = android_config
            else:
                raise InvalidDataError("Provided android_config is in the wrong format")

        if webpush_config:
            if isinstance(webpush_config, dict):
                fcm_payload["webpush"] = webpush_config
            else:
                raise InvalidDataError("Provided webpush_config is in the wrong format")

        if apns_config:
            if isinstance(apns_config, dict):
                fcm_payload["apns"] = apns_config
            else:
                raise InvalidDataError("Provided apns_config is in the wrong format")

        if fcm_options:
            if isinstance(fcm_options, dict):
                fcm_payload["fcm_options"] = fcm_options
            else:
                raise InvalidDataError("Provided fcm_options is in the wrong format")

        fcm_payload["notification"] = (
            {}
        )  # - https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#notification
        # If title is present, use it
        if notification_title:
            fcm_payload["notification"]["title"] = notification_title
        if notification_body:
            fcm_payload["notification"]["body"] = notification_body
        if notification_image:
            fcm_payload["notification"]["image"] = notification_image

        # Do this if you only want to send a data message.
        if data_payload and (not notification_title and not notification_body):
            del fcm_payload["notification"]

        return self.json_dumps({"message": fcm_payload, "validate_only": dry_run})
