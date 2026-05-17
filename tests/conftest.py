import json
from unittest.mock import AsyncMock

import pytest
from google.auth.credentials import Credentials

from pyfcm import FCMNotification
from pyfcm.baseapi import BaseAPI


class DummyCredentials(Credentials):
    def __init__(self):
        self.token = "dummy_token"
        self._expired = True

    def refresh(self, request):
        self.token = "refreshed_dummy_token"
        self._expired = False

    @property
    def expired(self):
        return self._expired


@pytest.fixture(scope="function")
def push_service():
    return FCMNotification(credentials=DummyCredentials(), project_id="test")


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


@pytest.fixture(scope="function")
def base_api():
    return BaseAPI(credentials=DummyCredentials(), project_id="test")
