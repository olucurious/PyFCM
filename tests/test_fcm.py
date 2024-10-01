import pytest
from pyfcm import FCMNotification, errors
import os
from google.oauth2 import service_account


def test_push_service_without_credentials():
    try:
        FCMNotification(service_account_file="", project_id="", credentials=None)
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass


def test_push_service_directly_passed_credentials():
    service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", None)
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=["https://www.googleapis.com/auth/firebase.messaging"],
    )
    push_service = FCMNotification(credentials=credentials)

    # We should infer the project ID/endpoint from credentials
    # without the need to explcitily pass it
    assert push_service.fcm_end_point == (
        "https://fcm.googleapis.com/v1/projects/"
        f"{credentials.project_id}/messages:send"
    )


def test_notify(push_service, generate_response):
    response = push_service.notify(
        fcm_token="Test",
        notification_body="Test",
        notification_title="Test",
        dry_run=True,
    )

    assert isinstance(response, dict)
