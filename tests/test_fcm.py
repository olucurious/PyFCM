from pyfcm import FCMNotification, errors


def test_push_service_without_credentials():
    try:
        FCMNotification(service_account_file=None, project_id=None, credentials=None)
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass

def test_push_service_with_incorrect_service_account_file():
    try:
        fcm = FCMNotification(service_account_file='./foo.json', project_id=None, credentials=None)
        fcm.notify()
        assert False, "Should raise InvalidDataError without correct service account file path"
    except errors.InvalidDataError:
        pass

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
