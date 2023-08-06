"""Central Token Service"""

import logging
from typing import Text, Optional, Dict, Any, List

from skill_sdk.intents import r
from skill_sdk.utils.access_token_helper import AccessTokenHelper
from skill_sdk.utils.util import CamelModel
from skill_sdk.services.base import BaseService

logger = logging.getLogger(__name__)

#
#   The models below reflect Central Token Service's (CTS) response structure
#


class TokenV2Dto(CamelModel):
    """Token DTO v2.0"""

    token_name: Text
    access_token: Text
    valid_until: Optional[Text]
    last_refresh_failure: Optional[Text]
    extra_info: Optional[Dict[Text, Any]]


class TokensV2Dto(CamelModel):
    """List of Token DTO v2.0"""

    tokens: List[TokenV2Dto]


class CentralTokenService(BaseService):
    """Central Token Service connector"""

    VERSION = 2
    NAME = "cts"

    async def get_token(
        self,
        token_name: Text,
    ) -> TokenV2Dto:
        """
        Get token: resolve the token for that particular tenant, access token and token name

        :param token_name:
        :return:
        """
        async with self.async_client as client:
            tenant = self.get_tenant_id_from_request_token()
            extra_headers = {"X-Consumer-Username": tenant}
            data = await client.get(f"{self.url}/api/v2/token/{token_name}", headers=extra_headers)
            return TokenV2Dto(**data.json())

    async def get_all_tokens(
        self,
    ) -> TokensV2Dto:
        """
        Get all tokens: resolve all tokens for that particular tenant and access token

        :return:
        """
        async with self.async_client as client:
            tenant = self.get_tenant_id_from_request_token()
            extra_headers = {"X-Consumer-Username": tenant}
            data = await client.get(f"{self.url}/api/v2/token", headers=extra_headers)
            return TokensV2Dto(**data.json())

    def get_tenant_id_from_request_token(self):
        token = r.svh_access_token
        access_token_helper = AccessTokenHelper(token)
        return access_token_helper.get("tenant")
