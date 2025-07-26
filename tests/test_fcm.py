from pyfcm import FCMNotification, errors


def test_push_service_without_credentials():
    try:
        FCMNotification(service_account_file=None, project_id=None, credentials=None)
        assert False, "Should raise AuthenticationError without credentials"
    except errors.AuthenticationError:
        pass


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
