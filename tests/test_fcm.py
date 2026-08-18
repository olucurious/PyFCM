import pytest

from pyfcm import FCMNotification, errors


def test_push_service_without_credentials():
    try:
        FCMNotification(service_account_file=None, project_id=None, credentials=None)
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass


def test_push_service_with_incorrect_service_account_file(tmp_path):
    missing_file = tmp_path / "missing.json"
    with pytest.raises(errors.InvalidDataError):
        fcm = FCMNotification(
            service_account_file=missing_file, project_id=None, credentials=None
        )
        fcm.notify()


def test_push_service_does_not_leak_credentials():
    raw_credentials = '{"private_key":"TOP-SECRET-PRIVATE-KEY"}'
    with pytest.raises(errors.InvalidDataError) as exc_info:
        fcm = FCMNotification(
            service_account_file=raw_credentials,
            project_id=None,
            credentials=None,
        )
        fcm._initialize_credentials()

    error_message = str(exc_info.value)
    assert raw_credentials not in error_message
    assert "TOP-SECRET-PRIVATE-KEY" not in error_message


def test_push_service_with_valid_service_account_file(mocker):
    # When the service account file exists, credentials must be built via
    # google.oauth2.service_account.Credentials.from_service_account_file.
    # google.oauth2.credentials.Credentials does not provide that method.
    mocker.patch("pyfcm.baseapi.path.isfile", return_value=True)
    mock_from_file = mocker.patch(
        "pyfcm.baseapi.service_account.Credentials.from_service_account_file",
        return_value="dummy-credentials",
    )

    fcm = FCMNotification(
        service_account_file="./service_account.json",
        project_id="test",
        credentials=None,
    )
    fcm._initialize_credentials()

    mock_from_file.assert_called_once_with(
        "./service_account.json",
        scopes=["https://www.googleapis.com/auth/firebase.messaging"],
    )
    assert fcm.credentials == "dummy-credentials"


def test_push_service_directly_passed_credentials(push_service):
    # We should infer the project ID/endpoint from credentials
    # without the need to explcitily pass it
    assert push_service.fcm_end_point == (
        "https://fcm.googleapis.com/v1/projects/"
        f"{push_service.credentials.project_id}/messages:send"
    )


def test_notify(push_service, generate_response):
    response = push_service.notify(
        fcm_token="Test",
        notification_body="Test",
        notification_title="Test",
        dry_run=True,
    )

    assert isinstance(response, dict)
