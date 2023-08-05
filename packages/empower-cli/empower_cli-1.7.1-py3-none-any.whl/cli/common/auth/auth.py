from string import Template
from typing import Any, Optional

import requests
from cli.common.auth.server import AuthCodeReceiver
from cli.common.schemas import Enterprise
from cli.common.store_client import StoreContainers, store

from .config import BROWSER_LOGIN_URL, HOST_NAME, PORT


class BrowserAuthManager:
    def __init__(self, domain: str):
        """CLI login for specified domain with a keycloak browser form."""
        self.domain = domain

    def browser_auth(self) -> None:
        """Process browser flow login."""
        with AuthCodeReceiver(host=HOST_NAME, port=PORT) as receiver:
            receiver.get_auth_response(auth_uri=self._get_auth_uri(), timeout=60)

    def _get_auth_uri(self) -> str:
        """Complete auth URI string with domain specified parameters:
        authServerUri, authRealm, authClientId, etc.
        """
        domain_auth_url_response = self.__get_domain_auth_url()
        api_config_response = self.__get_api_config(
            domain_auth_url_response.get("apiUrl")
        )
        return Template(BROWSER_LOGIN_URL).substitute(
            domain=domain_auth_url_response.get("authServerUrl"),
            realm=domain_auth_url_response.get("authRealm"),
            client_id=api_config_response.get("authClientId"),
        )

    def store_enterprise(self) -> None:
        enterprises = self.__parse_enterprise()
        default_environment = self.__get_default_environment(enterprises)
        store.save(
            StoreContainers.environment.value,
            enterprise=[enterprise.dict() for enterprise in enterprises],
        )
        store.save(
            StoreContainers.environment.value,
            default_environment=default_environment,
        )

    @staticmethod
    def __get_default_environment(
        enterprises: list[Enterprise],
    ) -> Optional[dict[str, Any]]:
        try:
            default_environment = enterprises[0].default_environment
        except IndexError:
            pass
        else:
            return default_environment.dict()

    def __parse_enterprise(self) -> list[Enterprise]:
        enterprise_response = requests.get(
            f"http://{store.empower_discovery_url}/"
            f"enterprise/oauth-domain/{self.domain}"
        )
        enterprise = [Enterprise(**item) for item in enterprise_response.json()]
        return enterprise

    def __get_domain_auth_url(self) -> dict[str, Any]:
        """Get domain auth info from Discovery service.

        :return: domain auth info response
        """
        auth_url_response = requests.get(
            f"http://{store.empower_discovery_url}/auth-url/{self.domain}"
        )
        auth_url_response.raise_for_status()
        return auth_url_response.json()

    @staticmethod
    def __get_api_config(api_url: str) -> dict[str, Any]:
        """Get configuration info for a given api instance.

        :param api_url: URL of an API instance
        :return: configuration endpoint response
        """
        api_config_response = requests.get(f"{api_url}/configuration")
        api_config_response.raise_for_status()
        return api_config_response.json()
