#
#
# voice-skill-sdk
#
# (C) 2021, Deutsche Telekom AG
#
# This file is distributed under the terms of the MIT license.
# For details see the file LICENSE in the top directory.
#
from typing import Optional, Text

from pydantic import Extra

from skill_sdk.responses.card import CardFacet
from skill_sdk.responses.touchpoint_instructions import TouchpointInstructionsFacet
from skill_sdk.utils.util import CamelModel


class PlainTextFacet(CamelModel):
    value: Text

    def __init__(self, value: Text):
        super().__init__(value=value)


class TtsFacet(CamelModel):
    ssml: Text


class EventHistoryFacet(CamelModel):
    target_device_id: Text


class VastFacet(CamelModel):
    masked_response: Text


class ResponseFacets(CamelModel):
    plain_text: PlainTextFacet

    tts: Optional[TtsFacet]

    card: Optional[CardFacet]

    touchpoint_instructions: Optional[TouchpointInstructionsFacet]

    event_history: Optional[EventHistoryFacet]

    vast: Optional[VastFacet]

    class Config:
        extra = Extra.allow
