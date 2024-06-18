import pytest
from pyfcm import FCMNotification, errors


def test_push_service_without_credentials():
    try:
        FCMNotification(service_account_file="", project_id="")
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass


def test_notify(push_service, generate_response):
    response = push_service.notify(
        fcm_token="Test",
        notification_body="Test",
        notification_title="Test",
        dry_run=True,
    )

    assert isinstance(response, dict)


def test_async_notify(push_service, mock_aiohttp_session):
    params = {
        "fcm_token": "test",
        "notification_title": "test",
        "notification_body": "test",
        "notification_image": "test",
        "data_payload": {"test": "test"},
        "topic_name": "test",
        "topic_condition": "test",
        "android_config": {},
        "apns_config": {},
        "webpush_config": {},
        "fcm_options": {},
        "dry_run": False,
    }

    params_list = [params for _ in range(100)]

    push_service.send_async_request(params_list, timeout=5)
