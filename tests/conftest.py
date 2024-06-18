import json
import os
from unittest.mock import AsyncMock

import pytest

from pyfcm import FCMNotification, errors
from pyfcm.baseapi import BaseAPI


@pytest.fixture(scope="module")
def push_service():
    service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", None)
    project_id = os.getenv("FCM_TEST_PROJECT_ID", None)
    assert (
        service_account_file
    ), "Please set the service_account for testing according to CONTRIBUTING.rst"

    return FCMNotification(
        service_account_file=service_account_file, project_id=project_id
    )


@pytest.fixture
def generate_response(mocker):
    response = {"test": "test"}
    mock_response = mocker.Mock()
    mock_response.json.return_value = response
    mock_response.status_code = 200
    mock_response.headers = {"Content-Length": "123"}
    mocker.patch("pyfcm.baseapi.BaseAPI.send_request", return_value=mock_response)


@pytest.fixture
def mock_aiohttp_session(mocker):
    # Define the fake response data
    response = {"test": "test"}

    # Create a mock response object
    mock_response = AsyncMock()
    mock_response.text = AsyncMock(return_value=json.dumps(response))
    mock_response.status = 200
    mock_response.headers = {"Content-Length": "123"}

    mock_send = mocker.patch("pyfcm.async_fcm.send_request", new_callable=AsyncMock)
    mock_send.return_value = mock_response
    return mock_send


@pytest.fixture(scope="module")
def base_api():
    service_account = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", None)
    assert (
        service_account
    ), "Please set the service_account for testing according to CONTRIBUTING.rst"

    return BaseAPI(api_key=service_account)
