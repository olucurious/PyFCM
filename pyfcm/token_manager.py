from functools import cached_property
import threading
from datetime import datetime, timedelta, timezone
from typing import Optional

from google.oauth2 import service_account
from google.auth.credentials import Credentials
import google.auth.transport.requests

from pyfcm.errors import AuthenticationError, InvalidDataError


class TokenManager:
    """
    Token management class extracted from BaseAPI.
    Handles authentication credentials and access token lifecycle.
    """

    def __init__(
        self,
        service_account_file: Optional[str] = None,
        project_id: Optional[str] = None,
        credentials: Optional[Credentials] = None,
    ):
        """
        Initialize TokenManager

        Args:
            service_account_file (str): path to service account JSON file
            project_id (str): project ID of Google account
            credentials (Credentials): Google auth credentials instance
        """
        if not (service_account_file or credentials):
            raise AuthenticationError(
                "Please provide a service account file path or credentials in the constructor"
            )

        self._service_account_file = service_account_file
        self._project_id = project_id
        self._provided_credentials = credentials

        # Shared token management across threads
        self._shared_token = None
        self._token_lock = threading.RLock()

    @cached_property
    def _credentials(self) -> Credentials:
        """
        Get authentication credentials

        Returns:
            Credentials: Google authentication credentials
        """
        if self._provided_credentials is not None:
            return self._provided_credentials

        credentials = service_account.Credentials.from_service_account_file(
            self._service_account_file,
            scopes=["https://www.googleapis.com/auth/firebase.messaging"],
        )
        # Service account credentials has project_id (others are not)
        self._project_id = credentials.project_id or self._project_id
        self._service_account_file = None
        return credentials

    @cached_property
    def project_id(self) -> str:
        """
        Get project ID

        Returns:
            str: Project ID

        Raises:
            RuntimeError: If project_id is not configured
        """
        # Read credentials to resolve project_id if needed
        _ = self._credentials
        if self._project_id is None:
            raise RuntimeError(
                "Please provide a project_id either explicitly or through Google credentials."
            )
        return self._project_id

    def _is_token_valid(self) -> bool:
        """
        Enhanced token validity check with fallback mechanisms.
        Combines expired property check with time-based validation.

        Returns:
            bool: True if token is valid, False otherwise
        """
        if not self._shared_token:
            return False

        if self._credentials.expired:
            return False

        # Fallback check: time-based validation with 5-minute buffer
        # This accounts for the 4-minute early expiration issue
        if (
            hasattr(self._credentials, "expiry")
            and self._credentials.expiry
            and self._credentials.expiry
            <= datetime.now(timezone.utc) + timedelta(minutes=5)
        ):
            return False

        return True

    def get_access_token(self) -> str:
        """
        Thread-safe access token management with shared token across threads.
        Uses double-checked locking pattern for performance with enhanced validation.

        Returns:
            str: Access token

        Raises:
            InvalidDataError: If token acquisition fails
        """
        # First check without lock (performance optimization)
        if self._is_token_valid():
            return self._shared_token

        # Acquire lock and check again (double-checked locking)
        with self._token_lock:
            if self._is_token_valid():
                return self._shared_token

            try:
                request = google.auth.transport.requests.Request()
                self._credentials.refresh(request)
                self._shared_token = self._credentials.token
                return self._shared_token
            except Exception as e:
                raise InvalidDataError(e)

    def refresh_token_if_expired(self) -> None:
        """
        Refresh token if needed
        """
        with self._token_lock:
            self._shared_token = None
            if self._credentials:
                try:
                    request = google.auth.transport.requests.Request()
                    self._credentials.refresh(request)
                except Exception:
                    # If refresh fails, let the next request handle it
                    pass
