import json
from typing import TYPE_CHECKING, Any, Dict

import requests

from .version import _user_agent

if TYPE_CHECKING:
    # Imports that happen below in methods to fix circular import dependency
    # issues need to also be specified here to satisfy mypy type checking.
    pass


class User:
    """A platform User."""

    def __init__(self, client, data: Dict[str, Any], standalone=False) -> None:
        self.client = client
        self._id = data["id"]
        self._email = data["email"] if "email" in data else "admin@keycloak"
        self._username = data["username"]
        self._enabled = data["enabled"]
        self._createdTimeastamp = data["createdTimestamp"]

    def __repr__(self):
        return f"""User({{"id": "{self.id()}", "email": "{self.email()}", "username": "{self.username()}", "enabled": "{self.enabled()})"""

    def id(self) -> str:
        return self._id

    def email(self) -> str:
        return self._email

    def username(self) -> str:
        return self._username

    def enabled(self) -> bool:
        return self._enabled

    @staticmethod
    def list_users(
        auth,
        api_endpoint: str = "http://api-lb:8080",
        auth_endpoint: str = "http://api-lb:8080",
    ):
        headers = {
            "authorization": auth._bearer_token_str(),
            "user-agent": _user_agent,
        }
        users = requests.post(
            f"{api_endpoint}/v1/api/users/query", data="{}", headers=headers
        )
        if users.status_code > 299:
            raise Exception("Failed to list exiting users.")
        return users.json()["users"].values()

    @staticmethod
    def invite_user(
        email,
        password,
        auth,
        api_endpoint: str = "http://api-lb:8080",
        auth_endpoint: str = "http://api-lb:8080",
    ):
        # TODO: Refactor User.list_users() here when this stabilizes

        headers = {
            "authorization": auth._bearer_token_str(),
            "user-agent": _user_agent,
        }
        users = requests.post(
            f"{api_endpoint}/v1/api/users/query", data=json.dumps({}), headers=headers
        )
        if users.status_code > 299:
            print(users.content)
            print(users.text)
            raise Exception("Failed to list exiting users.")
        existing_users = users.json()["users"].values()
        user_present = [user for user in existing_users if user["username"] == email]
        if len(user_present) == 0:
            data = {"email": email}
            if password:
                data["password"] = password
            user = response = users = requests.post(
                f"{api_endpoint}/v1/api/users/invite",
                json=data,
                headers=headers,
            ).json()
            return user
        else:
            return user_present[0]
