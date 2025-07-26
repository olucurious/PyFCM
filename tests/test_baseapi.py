import json
import time


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


def test_send_request_normal(base_api, mocker):
    """Test that send_request called once on success"""

    success_response = mocker.Mock()
    success_response.headers = {}

    mock_session = mocker.Mock()
    mock_session.post.side_effect = [success_response]

    base_api.thread_local = mocker.Mock()
    base_api.thread_local.requests_session = mock_session
    base_api.thread_local.token_expiry = time.time() + 1000

    # do
    result = base_api.send_request(payload="test_payload", timeout=30)

    # check
    assert mock_session.post.call_count == 1
    assert result == success_response


def test_send_request_retry_after(base_api, mocker):
    """Test that send_request retries when Retry-After header is present"""

    # Mock time.sleep to avoid actual delays
    mock_sleep = mocker.patch("time.sleep")

    retry_response = mocker.Mock()
    retry_response.headers = {"Retry-After": "2"}

    success_response = mocker.Mock()
    success_response.headers = {}

    mock_session = mocker.Mock()
    mock_session.post.side_effect = [retry_response, success_response]

    base_api.thread_local = mocker.Mock()
    base_api.thread_local.requests_session = mock_session
    base_api.thread_local.token_expiry = time.time() + 1000

    # do
    result = base_api.send_request(payload="test_payload", timeout=30)

    # check
    assert mock_session.post.call_count == 2
    mock_sleep.assert_called_once_with(2)
    assert result == success_response


def test_send_request_access_token_expired_retry(base_api, mocker):
    """Test that send_request retries when ACCESS_TOKEN_EXPIRED error occurs"""

    # Mock the expired token response
    EXPIRED_STATUS_CODE = 401
    expired_response = mocker.Mock()
    expired_response.status_code = EXPIRED_STATUS_CODE
    expired_response.headers = {}
    expired_response.json.return_value = {
        "error": {
            "code": EXPIRED_STATUS_CODE,
            "message": "Request had invalid authentication credentials.",
            "status": "UNAUTHENTICATED",
            "details": [
                {
                    "@type": "type.googleapis.com/google.rpc.ErrorInfo",
                    "reason": "ACCESS_TOKEN_EXPIRED",
                    "domain": "googleapis.com",
                }
            ],
        }
    }

    success_response = mocker.Mock()
    success_response.status_code = 200
    success_response.headers = {}

    mock_session = mocker.Mock()
    mock_session.post.side_effect = [expired_response, success_response]

    mock_requests_session = mocker.patch.object(
        type(base_api), "requests_session", new_callable=mocker.PropertyMock
    )
    mock_requests_session.return_value = mock_session

    # do
    result = base_api.send_request(payload="test_payload", timeout=30)

    # check
    assert mock_session.post.call_count == 2
    assert base_api.thread_local.token_expiry == 0
    assert result == success_response
