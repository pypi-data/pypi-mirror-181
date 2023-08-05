from typing import Any, Dict, Generator, List, Optional

import requests
from typing_extensions import TypedDict

from stytch.api.base import Base


class Operands(TypedDict):
    filter_name: str
    filter_value: Any


class SearchQuery(TypedDict):
    operator: str
    operands: List[Operands]


class Users(Base):
    @property
    def user_url(self) -> str:
        return self.get_url("users")

    def _validate_attributes(self, attributes: Dict[str, str]) -> bool:
        if not attributes:
            return True
        return self._validate_fields(
            set(["ip_address", "user_agent"]), set(attributes.keys())
        )

    def create(
        self,
        email: Optional[str] = None,
        phone_number: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        create_user_as_pending: bool = False,
        attributes: Optional[Dict[str, str]] = None,
        trusted_metadata: Optional[Dict[str, Any]] = None,
        untrusted_metadata: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        data: Dict[str, Any] = {
            "email": email,
            "phone_number": phone_number,
            "name": {
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
            },
            "create_user_as_pending": create_user_as_pending,
            "trusted_metadata": trusted_metadata,
            "untrusted_metadata": untrusted_metadata,
        }
        if attributes and self._validate_attributes(attributes):
            data.update({"attributes": attributes})
        return self._post("{0}".format(self.user_url), data)

    def get(self, user_id: str) -> requests.Response:
        return self._get("{0}/{1}".format(self.user_url, user_id))

    def get_pending(
        self, limit: Optional[int] = None, starting_after_id: Optional[str] = None
    ) -> requests.Response:
        query_params = {}
        if limit:
            query_params.update({"limit": str(limit)})
        if starting_after_id:
            query_params.update({"starting_after_id": starting_after_id})

        return self._get("{0}/{1}".format(self.user_url, "pending"), query_params)

    def search(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        query: Optional[SearchQuery] = None,
    ) -> requests.Response:
        data: Dict[str, Any] = {}

        if limit is not None:
            data["limit"] = limit
        if cursor is not None:
            data["cursor"] = cursor
        if query is not None:
            data["query"] = query

        return self._post("{0}/{1}".format(self.user_url, "search"), data)

    def search_all(
        self,
        limit: Optional[int] = None,
        cursor: Optional[str] = None,
        query: Optional[SearchQuery] = None,
    ) -> Generator[requests.Response, None, None]:
        while True:
            results = self.search(limit, cursor, query)
            yield results
            cursor = results.json()["results_metadata"]["next_cursor"]
            if cursor is None:
                break

    def delete(self, user_id: str) -> requests.Response:
        return self._delete("{0}/{1}".format(self.user_url, user_id))

    def update(
        self,
        user_id: str,
        emails: Optional[List[str]] = None,
        phone_numbers: Optional[List[str]] = None,
        crypto_wallets: Optional[List[Dict[str, str]]] = None,
        first_name: Optional[str] = None,
        middle_name: Optional[str] = None,
        last_name: Optional[str] = None,
        attributes: Optional[Dict[str, str]] = None,
        trusted_metadata: Optional[Dict[str, Any]] = None,
        untrusted_metadata: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        data: Dict[str, Any] = {}
        name = {}
        if first_name:
            name.update({"first_name": first_name})
        if middle_name:
            name.update({"middle_name": middle_name})
        if last_name:
            name.update({"last_name": last_name})
        if name:
            data.update({"name": name})
        if crypto_wallets:
            data.update({"crypto_wallets": crypto_wallets})

        if emails:
            ems = []
            for email in emails:
                ems.append({"email": email})
            data.update({"emails": ems})

        if phone_numbers:
            pns = []
            for phone_number in phone_numbers:
                pns.append({"phone_number": phone_number})
            data.update({"phone_numbers": pns})

        if attributes and self._validate_attributes(attributes):
            data.update({"attributes": attributes})

        if trusted_metadata:
            data.update({"trusted_metadata": trusted_metadata})
        if untrusted_metadata:
            data.update({"untrusted_metadata": untrusted_metadata})

        return self._put("{0}/{1}".format(self.user_url, user_id), data)

    def delete_email(self, email_id: str) -> requests.Response:
        return self._delete("{0}/emails/{1}".format(self.user_url, email_id))

    def delete_phone_number(self, phone_id: str) -> requests.Response:
        return self._delete("{0}/phone_numbers/{1}".format(self.user_url, phone_id))

    def delete_webauthn_registration(
        self, webauthn_registration: str
    ) -> requests.Response:
        return self._delete(
            "{0}/webauthn_registrations/{1}".format(
                self.user_url, webauthn_registration
            )
        )

    def delete_totp(self, totp_id: str) -> requests.Response:
        return self._delete("{0}/totps/{1}".format(self.user_url, totp_id))

    def delete_crypto_wallet(self, crypto_wallet_id: str) -> requests.Response:
        return self._delete(
            "{0}/crypto_wallets/{1}".format(self.user_url, crypto_wallet_id)
        )

    def delete_password(self, password_id: str) -> requests.Response:
        return self._delete("{0}/passwords/{1}".format(self.user_url, password_id))

    def delete_biometric_registration(
        self, biometric_registration_id: str
    ) -> requests.Response:
        return self._delete(
            "{0}/biometric_registrations/{1}".format(
                self.user_url, biometric_registration_id
            )
        )

    def delete_oauth_user_registration(
        self, oauth_user_registration_id: str
    ) -> requests.Response:
        return self._delete(
            "{0}/oauth/{1}".format(self.user_url, oauth_user_registration_id)
        )
