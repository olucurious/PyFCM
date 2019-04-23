import os
import json
import pytest

from pyfcm import errors
from pyfcm.baseapi import BaseAPI


@pytest.fixture(scope="module")
def base_api():
    api_key = os.getenv("FCM_TEST_API_KEY", None)
    assert api_key, "Please set the environment variables for testing according to CONTRIBUTING.rst"

    return BaseAPI(api_key=api_key)


def test_init_baseapi():
    try:
        BaseAPI()
        assert False, "Should raise AuthenticationError"
    except errors.AuthenticationError:
        pass


def test_request_headers(base_api):
    headers = base_api.request_headers()

    assert headers["Content-Type"] == "application/json"
    assert headers["Authorization"] == "key=" + os.getenv("FCM_TEST_API_KEY")


def test_registration_id_chunks(base_api):
    registrations_ids = range(9999)
    chunks = list(base_api.registration_id_chunks(registrations_ids))

    assert len(chunks) == 10
    assert len(chunks[0]) == 1000
    assert len(chunks[-1]) == 999


def test_json_dumps(base_api):
    json_string = base_api.json_dumps(
        [
            {"test": "Test"},
            {"test2": "Test2"}
        ]
    )

    assert json_string == b"[{\"test\":\"Test\"},{\"test2\":\"Test2\"}]"


def test_parse_payload(base_api):
    json_string = base_api.parse_payload(
        registration_ids=["Test"],
        message_body="Test",
        message_title="Test",
        message_icon="Test",
        sound="Test",
        collapse_key="Test",
        delay_while_idle=False,
        time_to_live=0,
        restricted_package_name="Test",
        low_priority=False,
        dry_run=False,
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

    data = json.loads(json_string.decode("utf-8"))

    assert data["notification"] == {
        "android_channel_id": "Test",
        "body": "Test",
        "click_action": "Test",
        "color": "Test",
        "icon": "Test",
        "sound": "Test",
        "tag": "Test",
        "title": "Test"
    }

    assert 'time_to_live' in data
    assert data['time_to_live'] == 0


def test_clean_registration_ids(base_api):
    registrations_ids = base_api.clean_registration_ids(["Test"])
    assert len(registrations_ids) == 0


def test_subscribe_registration_ids_to_topic(base_api):
    # TODO
    pass


def test_unsubscribe_registration_ids_from_topic(base_api):
    # TODO
    pass


def test_parse_responses(base_api):
    response = base_api.parse_responses()

    assert response == {
        "multicast_ids": [],
        "success": 0,
        "failure": 0,
        "canonical_ids": 0,
        "results": [],
        "topic_message_id": None
    }
