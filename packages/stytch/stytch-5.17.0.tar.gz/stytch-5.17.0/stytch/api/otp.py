from typing import TYPE_CHECKING, Any, Dict, Optional

import requests

from stytch.api.base import Base, _validate_attributes

if TYPE_CHECKING:
    from stytch.client import Client


class OTP(Base):
    def __init__(self, client: "Client") -> None:
        super().__init__(client)
        self.email = Email(client)
        self.sms = SMS(client)
        self.whatsapp = Whatsapp(client)

    @property
    def otp_url(self) -> str:
        return self.get_url("otps")

    def authenticate(
        self,
        method_id: str,
        code: str,
        attributes: Optional[Dict[str, str]] = None,
        options: Optional[Dict[str, bool]] = None,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
        session_duration_minutes: Optional[int] = None,
        session_custom_claims: Optional[Dict[str, Any]] = None,
    ) -> requests.Response:
        if attributes:
            attributes = _validate_attributes(attributes)

        if options:
            options = self._validate_options(options)

        data: Dict[str, Any] = {
            "method_id": method_id,
            "code": code,
        }
        if attributes:
            data["attributes"] = attributes
        if options:
            data["options"] = options
        if session_token:
            data["session_token"] = session_token
        if session_jwt:
            data["session_jwt"] = session_jwt
        if session_duration_minutes:
            data["session_duration_minutes"] = session_duration_minutes
        if session_custom_claims:
            data["session_custom_claims"] = session_custom_claims

        return self._post(
            "{0}/authenticate".format(
                self.otp_url,
            ),
            data=data,
        )


class SMS(Base):
    @property
    def otp_url(self) -> str:
        return self.get_url("otps")

    def send(
        self,
        phone_number: str,
        expiration_minutes: Optional[int] = None,
        attributes: Optional[Dict[str, str]] = None,
        locale: Optional[str] = None,
        user_id: Optional[str] = None,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
    ) -> requests.Response:
        if attributes:
            attributes = _validate_attributes(attributes)

        data: Dict[str, Any] = {
            "phone_number": phone_number,
        }
        if expiration_minutes:
            data["expiration_minutes"] = expiration_minutes
        if attributes:
            data["attributes"] = attributes
        if locale:
            data["locale"] = locale
        if user_id:
            data["user_id"] = user_id
        if session_token:
            data["session_token"] = session_token
        if session_jwt:
            data["session_jwt"] = session_jwt

        return self._post(
            "{0}/sms/send".format(
                self.otp_url,
            ),
            data=data,
        )

    def login_or_create(
        self,
        phone_number: str,
        expiration_minutes: Optional[int] = None,
        attributes: Optional[Dict[str, str]] = None,
        create_user_as_pending: bool = False,
        locale: Optional[str] = None,
    ) -> requests.Response:
        if attributes:
            attributes = _validate_attributes(attributes)

        data: Dict[str, Any] = {
            "phone_number": phone_number,
            "create_user_as_pending": create_user_as_pending,
        }
        if expiration_minutes:
            data["expiration_minutes"] = expiration_minutes
        if attributes:
            data["attributes"] = attributes
        if locale:
            data["locale"] = locale

        return self._post(
            "{0}/sms/login_or_create".format(
                self.otp_url,
            ),
            data=data,
        )


class Whatsapp(Base):
    @property
    def otp_url(self) -> str:
        return self.get_url("otps")

    def send(
        self,
        phone_number: str,
        expiration_minutes: Optional[int] = None,
        attributes: Optional[Dict[str, str]] = None,
        locale: Optional[str] = None,
        user_id: Optional[str] = None,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
    ) -> requests.Response:
        if attributes:
            attributes = _validate_attributes(attributes)

        data: Dict[str, Any] = {
            "phone_number": phone_number,
        }
        if expiration_minutes:
            data["expiration_minutes"] = expiration_minutes
        if attributes:
            data["attributes"] = attributes
        if locale:
            data["locale"] = locale
        if user_id:
            data["user_id"] = user_id
        if session_token:
            data["session_token"] = session_token
        if session_jwt:
            data["session_jwt"] = session_jwt

        return self._post(
            "{0}/whatsapp/send".format(
                self.otp_url,
            ),
            data=data,
        )

    def login_or_create(
        self,
        phone_number: str,
        expiration_minutes: Optional[int] = None,
        attributes: Optional[Dict[str, str]] = None,
        create_user_as_pending: bool = False,
        locale: Optional[str] = None,
    ) -> requests.Response:
        if attributes:
            attributes = _validate_attributes(attributes)

        data: Dict[str, Any] = {
            "phone_number": phone_number,
            "create_user_as_pending": create_user_as_pending,
        }
        if expiration_minutes:
            data["expiration_minutes"] = expiration_minutes
        if attributes:
            data["attributes"] = attributes
        if locale:
            data["locale"] = locale

        return self._post(
            "{0}/whatsapp/login_or_create".format(
                self.otp_url,
            ),
            data=data,
        )


class Email(Base):
    @property
    def otp_url(self) -> str:
        return self.get_url("otps")

    def send(
        self,
        email: str,
        expiration_minutes: Optional[int] = None,
        attributes: Optional[Dict[str, str]] = None,
        locale: Optional[str] = None,
        user_id: Optional[str] = None,
        session_token: Optional[str] = None,
        session_jwt: Optional[str] = None,
    ) -> requests.Response:
        if attributes:
            attributes = _validate_attributes(attributes)

        data: Dict[str, Any] = {
            "email": email,
        }
        if expiration_minutes:
            data["expiration_minutes"] = expiration_minutes
        if attributes:
            data["attributes"] = attributes
        if locale:
            data["locale"] = locale
        if user_id:
            data["user_id"] = user_id
        if session_token:
            data["session_token"] = session_token
        if session_jwt:
            data["session_jwt"] = session_jwt

        return self._post(
            "{0}/email/send".format(
                self.otp_url,
            ),
            data=data,
        )

    def login_or_create(
        self,
        email: str,
        expiration_minutes: Optional[int] = None,
        attributes: Optional[Dict[str, str]] = None,
        create_user_as_pending: bool = False,
        locale: Optional[str] = None,
    ) -> requests.Response:
        if attributes:
            attributes = _validate_attributes(attributes)

        data: Dict[str, Any] = {
            "email": email,
            "create_user_as_pending": create_user_as_pending,
        }
        if expiration_minutes:
            data["expiration_minutes"] = expiration_minutes
        if attributes:
            data["attributes"] = attributes
        if locale:
            data["locale"] = locale

        return self._post(
            "{0}/email/login_or_create".format(
                self.otp_url,
            ),
            data=data,
        )
