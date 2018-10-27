import os
import pytest

from pyfcm import FCMNotification, errors


@pytest.fixture(scope="module")
def push_service():
    api_key = os.getenv("FCM_TEST_API_KEY", None)
    assert api_key, "Please set the environment variables for testing according to CONTRIBUTING.rst"

    return FCMNotification(api_key=api_key)


def test_push_service_without_credentials():
    try:
        FCMNotification()
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass


def test_notify_single_device(push_service):
    try:
        push_service.notify_single_device(
            message_body="Test",
            dry_run=True
        )
        assert False, "Should raise InvalidDataError without registration id"
    except errors.InvalidDataError:
        pass

    response = push_service.notify_single_device(
        registration_id="Test",
        message_body="Test",
        message_title="Test",
        dry_run=True
    )

    assert isinstance(response, dict)


def test_single_device_data_message(push_service):
    try:
        push_service.single_device_data_message(
            data_message={"test": "Test"},
            dry_run=True
        )
        assert False, "Should raise InvalidDataError without registration id"
    except errors.InvalidDataError:
        pass

    response = push_service.single_device_data_message(
        registration_id="Test",
        data_message={"test": "Test"},
        dry_run=True
    )

    assert isinstance(response, dict)


def test_notify_multiple_devices(push_service):
    try:
        push_service.notify_multiple_devices(
            message_body="Test",
            dry_run=True
        )
        assert False, "Should raise InvalidDataError without registration id"
    except errors.InvalidDataError:
        pass

    response = push_service.notify_multiple_devices(
        registration_ids=["Test"],
        message_body="Test",
        message_title="Test",
        dry_run=True
    )

    assert isinstance(response, dict)


def test_multiple_devices_data_message(push_service):
    try:
        push_service.multiple_devices_data_message(
            data_message={"test": "Test"},
            dry_run=True
        )
        assert False, "Should raise InvalidDataError without registration ids"
    except errors.InvalidDataError:
        pass

    response = push_service.multiple_devices_data_message(
        registration_ids=["Test"],
        data_message={"test": "Test"},
        dry_run=True
    )

    assert isinstance(response, dict)


def test_notify_topic_subscribers(push_service):
    try:
        push_service.notify_topic_subscribers(
            message_body="Test",
            dry_run=True
        )
        assert False, "Should raise InvalidDataError without topic"
    except errors.InvalidDataError:
        pass

    response = push_service.notify_topic_subscribers(
        topic_name="test",
        message_body="Test",
        message_title="Test",
        dry_run=True
    )

    assert isinstance(response, dict)


def test_notify_with_args(push_service):
    push_service.notify_single_device(
        registration_id="Test",
        message_body="Test",
        message_title="Test",
        message_icon="Test",
        sound="Test",
        collapse_key="Test",
        delay_while_idle=False,
        time_to_live=100,
        restricted_package_name="Test",
        low_priority=False,
        dry_run=True,
        data_message={"test": "test"},
        click_action="Test",
        badge="Test",
        color="Test",
        tag="Test",
        body_loc_key="Test",
        body_loc_args="Test",
        title_loc_key="Test",
        title_loc_args="Test",
        content_available="Test",
        android_channel_id="Test",
        timeout=5,
        extra_notification_kwargs={},
        extra_kwargs={}
    )
