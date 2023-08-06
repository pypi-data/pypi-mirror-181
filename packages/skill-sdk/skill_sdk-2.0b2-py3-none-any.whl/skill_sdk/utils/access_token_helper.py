#
# voice-skill-sdk
#
# (C) 2022, Deutsche Telekom AG
#
# This file is distributed under the terms of the MIT license.
# For details see the file LICENSE in the top directory.
#
#
from enum import Enum
from typing import Union, Optional

import jwt

_access_token_userId = "sub"
_access_token_tenant = "tenant"


class SvhTokenKey(Enum):
    USER_ID = "sub"
    PROFILE = "profile"
    LOCALE = "locale"
    NOT_BEFORE_TIME = "nbf"
    USERTYPE = "userType"
    EXPIRY = "exp"
    TERMS_AND_CONDITIONS = "tncs"
    ISSUE_TIME = "iat"
    TENANT = "tenant"
    TRACKING_ID = "trackingId"
    ISSUER = "iss"
    AUDIENCES = "aud"
    TRACING_ENABLED = "tracing"
    TESTING = "testing"
    TRACING_UNTIL = "tracingUntil"
    DEVICE_SERIAL_NUMBER = "deviceSerialNumber"


class AccessTokenHelper:
    """
    Utility class responsible for retrieving svh access token information.

    NOTE :: Please do not store the user related token claims
            in any permanent persistence storage due to GDR compliance issues.
            Currently, there is not any existing mechanism for cleaning up any user related data.
    """

    def __init__(self, access_token: str):
        """
        Accepts an access token and decodes its payload

        :Raises DecodeError:
            if the jwt decode (not verification) fails for any reason
        """
        self.access_token = access_token
        self.payload = jwt.decode(self.access_token, options={"verify_signature": False})

    def get(self, key: Union[SvhTokenKey, str]) -> Optional[str]:
        """
        Returns the value of the given key from the provided access token

        :param key:
            It can be either an enum of type SvhTokenKey
            or a string of the desired key

        :return:
            the optional value of the provided key
        """
        shv_token_key = key.value if isinstance(key, SvhTokenKey) else key
        return self.payload.get(shv_token_key, None)
