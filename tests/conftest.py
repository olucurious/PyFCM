import json
from unittest.mock import AsyncMock

import pytest

from pyfcm import FCMNotification
from pyfcm.baseapi import BaseAPI
from google.auth.credentials import Credentials


class DummyCredentials(Credentials):
    def refresh():
        pass

    @property
    def project_id(self):
        return "test"


@pytest.fixture(scope="module")
def push_service():
    return FCMNotification(credentials=DummyCredentials())


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
    return BaseAPI(credentials=DummyCredentials())
