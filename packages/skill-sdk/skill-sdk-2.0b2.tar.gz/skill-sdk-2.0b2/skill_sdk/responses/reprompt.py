#
#
# voice-skill-sdk
#
# (C) 2021, Deutsche Telekom AG
#
# This file is distributed under the terms of the MIT license.
# For details see the file LICENSE in the top directory.
#

"""Re-prompt response"""

from typing import Optional, Text, Dict, Any, Union
from pydantic import validator

from skill_sdk.intents import request

from skill_sdk.responses.response import (
    ResponseFacets,
    PlainTextFacet,
    SkillInvokeResponse,
    ResponseType,
)


class Reprompt(SkillInvokeResponse):
    """
    Re-prompt response is sent to user as a measure to limit a number of re-prompts

    """

    # Response type defaults to ASK
    response_type: ResponseType = ResponseType.ASK

    # stop text will be sent if number of re-prompts is higher than maximum number
    stop_text: Optional[Text]

    # entity name if re-prompt is used for intent/entity
    entity: Optional[Text]

    # maximum number of re-prompts
    max_reprompts: int

    @validator("max_reprompts")
    def check_max_reprompts(cls, max_reprompts, values):
        # Name of the counter formatted as INTENT_ENTITY_reprompt_count
        entity = values.get("entity")
        name = (
            f"{request.intent}{'_' + entity if entity else ''}_reprompt_count"
        )

        try:
            reprompt_count = int(request.session.attributes[name]) + 1
        except (KeyError, ValueError):
            reprompt_count = 1

        if reprompt_count > max_reprompts > 0:
            del request.session.attributes[name]
            response_facets: ResponseFacets = values["response_facets"]
            values["response_facets"] = response_facets.copy(
                update=dict(plain_text=PlainTextFacet(values["stop_text"])))
            values["response_type"] = ResponseType.TELL
        else:
            request.session.attributes[name] = reprompt_count

        return max_reprompts

    def __init__(
        self,
        data: Union[Text, ResponseFacets],
        stop_text: Text = None,
        max_reprompts: int = 0,
        entity: Text = None,
        **kwargs,
    ) -> None:
        super().__init__(
            data=data,
            stop_text=stop_text,
            max_reprompts=max_reprompts,
            entity=entity,
            **kwargs,
        )

    def dict(self, *args, **kwargs) -> Dict[Text, Any]:
        return super(Reprompt, self).dict()
