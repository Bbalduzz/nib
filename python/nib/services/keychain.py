"""Keychain service for secure credential storage.

Provides secure storage for passwords, tokens, and other sensitive data
using the macOS Keychain.

Example:
    Store and retrieve a password::

        # Store a password
        app.keychain.set("MyApp", "user@example.com", "secret123")

        # Retrieve a password
        password = app.keychain.get("MyApp", "user@example.com")
"""

from typing import TYPE_CHECKING, Optional

from .base import Service

if TYPE_CHECKING:
    from ..core.app import App


class Keychain(Service):
    """Service for secure credential storage using macOS Keychain.

    Access via app.keychain property.

    The Keychain service provides secure storage for sensitive data like
    passwords, API tokens, and other credentials. Data is encrypted and
    stored in the system keychain.

    Example:
        Store and retrieve credentials::

            # Store a password
            app.keychain.set("MyApp", "user@example.com", "secret123")

            # Retrieve it later
            password = app.keychain.get("MyApp", "user@example.com")
            if password:
                print(f"Password: {password}")

            # Check if exists
            if app.keychain.exists("MyApp", "user@example.com"):
                print("Credential exists")

            # Delete when done
            app.keychain.delete("MyApp", "user@example.com")
    """

    def get(self, service: str, account: str) -> Optional[str]:
        """Retrieve a password from the keychain.

        Args:
            service: Service name (usually your app identifier).
            account: Account name (username, email, etc.).

        Returns:
            The password if found, None otherwise.
        """
        data = self._request(
            "keychain", "get",
            params={"service": service, "account": account},
        )
        return data.get("password")

    def set(self, service: str, account: str, password: str) -> bool:
        """Store a password in the keychain.

        If an entry already exists for the service/account combination,
        it will be updated.

        Args:
            service: Service name (usually your app identifier).
            account: Account name (username, email, etc.).
            password: The password/secret to store.

        Returns:
            True if stored successfully.
        """
        data = self._request(
            "keychain", "set",
            params={"service": service, "account": account, "password": password},
        )
        return data.get("success", False)

    def delete(self, service: str, account: str) -> bool:
        """Delete a password from the keychain.

        Args:
            service: Service name.
            account: Account name.

        Returns:
            True if deleted successfully.
        """
        data = self._request(
            "keychain", "delete",
            params={"service": service, "account": account},
        )
        return data.get("success", False)

    def exists(self, service: str, account: str) -> bool:
        """Check if a keychain entry exists.

        Args:
            service: Service name.
            account: Account name.

        Returns:
            True if exists, False otherwise.
        """
        data = self._request(
            "keychain", "exists",
            params={"service": service, "account": account},
        )
        return data.get("exists", False)
