import threading

import pytest
from google.auth.credentials import Credentials

from pyfcm.errors import InvalidDataError
from pyfcm.token_manager import TokenManager


class DummyCredentials(Credentials):
    def __init__(self):
        self.token = "initial_token"
        self._expired = True

    def refresh(self, request):
        self.token = "refreshed_token"
        self._expired = False

    @property
    def expired(self):
        return self._expired


@pytest.fixture
def token_manager():
    return TokenManager(credentials=DummyCredentials(), project_id="test")


class TestRefreshTokenIfExpired:
    def test_updates_shared_token_after_refresh(self, token_manager):
        """Regression: refresh_token_if_expired() must update _shared_token after refresh"""
        token_manager.refresh_token_if_expired()

        assert token_manager._shared_token == "refreshed_token"

    def test_no_double_refresh_on_subsequent_get_access_token(self, token_manager, mocker):
        """Regression: get_access_token() after refresh_token_if_expired() must not trigger a second refresh"""
        token_manager.refresh_token_if_expired()

        mock_refresh = mocker.patch.object(token_manager._credentials, "refresh")
        token_manager.get_access_token()

        mock_refresh.assert_not_called()

    def test_clears_shared_token_on_refresh_failure(self, token_manager, mocker):
        mocker.patch.object(
            token_manager._credentials, "refresh", side_effect=Exception("network error")
        )

        token_manager._shared_token = "old_token"
        token_manager.refresh_token_if_expired()

        assert token_manager._shared_token is None


class TestGetAccessToken:
    def test_returns_cached_token_without_refresh(self, token_manager, mocker):
        """Must return the cached token without calling credentials.refresh()"""
        token_manager._shared_token = "cached_token"
        token_manager._credentials._expired = False

        mock_refresh = mocker.patch.object(token_manager._credentials, "refresh")
        result = token_manager.get_access_token()

        assert result == "cached_token"
        mock_refresh.assert_not_called()

    def test_refreshes_and_returns_token_when_none(self, token_manager):
        """Must call credentials.refresh() and return the new token when _shared_token is None"""
        assert token_manager._shared_token is None

        result = token_manager.get_access_token()

        assert result == "refreshed_token"
        assert token_manager._shared_token == "refreshed_token"

    def test_raises_invalid_data_error_on_refresh_failure(self, token_manager, mocker):
        mocker.patch.object(
            token_manager._credentials, "refresh", side_effect=Exception("auth failed")
        )

        with pytest.raises(InvalidDataError):
            token_manager.get_access_token()

    def test_thread_safe_single_refresh_under_concurrent_calls(self, token_manager):
        """credentials.refresh() must be called only once even under concurrent calls from multiple threads"""
        refresh_count = 0
        original_refresh = token_manager._credentials.refresh

        def counting_refresh(request):
            nonlocal refresh_count
            refresh_count += 1
            original_refresh(request)

        token_manager._credentials.refresh = counting_refresh

        threads = [threading.Thread(target=token_manager.get_access_token) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert token_manager._shared_token == "refreshed_token"
        assert refresh_count == 1
