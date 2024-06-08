import os
import json
import pytest

from pyfcm import errors
from pyfcm.v1.baseapi import BaseAPI


@pytest.fixture(scope="module")
def base_api():
    service_account_file_path = "service_account.json"
    project_id = os.getenv("FCM_TEST_PROJECT_ID", None)
    assert (
        project_id
    ), "Please set the environment variables for testing according to CONTRIBUTING.rst"

    return BaseAPI(
        service_account_file_path=service_account_file_path, project_id=project_id
    )


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
        extra_kwargs={},
    )

    data = json.loads(json_string.decode("utf-8"))
    assert data["message"]["notification"] == {
        "android_channel_id": "Test",
        "badge": "Test",
        "body": "Test",
        "click_action": "Test",
        "color": "Test",
        "extra_kwargs": {},
        "extra_notification_kwargs": {},
        "icon": "Test",
        "sound": "Test",
        "tag": "Test",
        "timeout": 5,
        "title": "Test",
    }


def test_parse_responses(base_api):
    response = base_api.parse_responses()

    assert response == {
        "multicast_ids": [],
        "success": 0,
        "failure": 0,
        "canonical_ids": 0,
        "results": [],
        "topic_message_id": None,
    }
