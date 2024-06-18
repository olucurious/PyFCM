import os
import json
import pytest

from pyfcm import errors
from pyfcm.baseapi import BaseAPI


@pytest.fixture(scope="module")
def base_api():
    service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", None)
    project_id = os.getenv("FCM_TEST_PROJECT_ID", None)
    assert (
        project_id
    ), "Please set the environment variables for testing according to CONTRIBUTING.rst"

    return BaseAPI(service_account_file=service_account_file, project_id=project_id)


def test_json_dumps(base_api):
    json_string = base_api.json_dumps([{"test": "Test"}, {"test2": "Test2"}])

    assert json_string == b'[{"test":"Test"},{"test2":"Test2"}]'


def test_parse_payload(base_api):
    json_string = base_api.parse_payload(
        fcm_token="test",
        notification_title="test",
        notification_body="test",
        notification_image="test",
        data_payload={"test": "test"},
        topic_name="test",
        topic_condition="test",
        android_config={},
        apns_config={},
        webpush_config={},
        fcm_options={},
        dry_run=False,
    )

    data = json.loads(json_string.decode("utf-8"))

    assert data["message"]["notification"] == {
        "body": "test",
        "title": "test",
        "image": "test",
    }

    assert data["message"]["data"] == {"test": "test"}
