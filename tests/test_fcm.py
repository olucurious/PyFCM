import json
import pdb
from pyfcm import FCMNotification, errors

def test_credentials():
    return {
        "type": "service_account",
        "project_id": "my-project-123456",
        "private_key_id": "abc123def4567890abc123def4567890abc123de",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC...\n...REDACTED...\n-----END PRIVATE KEY-----\n",
        "client_email": "my-service-account@my-project-123456.iam.gserviceaccount.com",
        "client_id": "123456789012345678901",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-service-account%40my-project-123456.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com",
    }


def test_push_service_without_credentials():
    try:
        FCMNotification(service_account_file=None, project_id=None, credentials=None)
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass


def test_push_service_with_incorrect_service_account_file():
    try:
        fcm = FCMNotification(
            service_account_file="./foo.json", project_id=None, credentials=None
        )
        fcm.notify()
        assert False, (
            "Should raise InvalidDataError without correct service account file path"
        )
    except errors.InvalidDataError:
        pass


def test_push_works_with_dict_credentials(mocker):
    credentials = test_credentials()
    mock_from_info = mocker.patch(
        "pyfcm.baseapi.service_account.Credentials.from_service_account_info",
        return_value=credentials
    )

    fcm = FCMNotification(
        service_account_file=credentials,
        project_id="test",
        credentials=None,
    )
    fcm._initialize_credentials()

    mock_from_info.assert_called_once()
    assert fcm.credentials == credentials


def test_push_service_does_not_leak_credentials():
    import pytest
    credentials = test_credentials()
    with pytest.raises(errors.InvalidDataError) as exc_info:
        fcm = FCMNotification(
            service_account_file=json.dumps(credentials),
            project_id=None,
            credentials=None,
        )
        fcm.notify()

    error_message = str(exc_info.value)
    credentials = test_credentials()
    
    assert credentials["private_key"] not in error_message
    assert credentials["private_key_id"] not in error_message


def test_push_service_with_valid_service_account_file(mocker):
    # When the service account file exists, test_credentials must be built via
    # google.oauth2.service_account.test_credentials.from_service_account_file.
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

    mock_from_file.assert_called_once()
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
