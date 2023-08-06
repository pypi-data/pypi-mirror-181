#
#
# voice-skill-sdk
#
# (C) 2021, Deutsche Telekom AG
#
# This file is distributed under the terms of the MIT license.
# For details see the file LICENSE in the top directory.
#

"""Skill invoke response"""

import copy
from enum import Enum
from typing import Any, Dict, Optional, List, Text, Union

from skill_sdk.responses.response_facets import ResponseFacets, PlainTextFacet, EventHistoryFacet, VastFacet, TtsFacet
from skill_sdk.utils.util import CamelModel
from skill_sdk.responses.card import CardFacet, ListSection
from skill_sdk.responses.command import Command
from skill_sdk.responses.touchpoint_instructions import TouchpointInstructionsFacet
from skill_sdk.responses.task import ClientTask


class ResponseType(str, Enum):
    """
    Response types:

        TELL    pronounce the text on the device and end the session

        ASK     pronounce the text and wait for user's intent as response

        ASK_FREETEXT    pronounce the text and wait for user response as text

    """

    TELL = "TELL"
    ASK = "ASK"
    ASK_FREETEXT = "ASK_FREETEXT"


class SessionResponse(CamelModel):
    """Session attributes in the response"""

    attributes: Dict[Text, Text]


class SkillInvokeResponse(CamelModel):
    """Skill invoke response"""

    response_facets: ResponseFacets

    # Response type
    response_type: ResponseType = ResponseType.TELL

    # Device session
    session: Optional[SessionResponse]

    def __init__(
            self,
            data: Union[Text, ResponseFacets],
            response_type: Optional[ResponseType] = None,
            **kwargs) -> None:
        """
        :param data:            a full ResponseFacets object, or a simple text to fill a PlainTextFacet
        :param response_type:   response type
        :param kwargs:
        """

        response_facets = ResponseFacets(plain_text=PlainTextFacet(data)) if isinstance(data, str) else data
        response: Dict[Text, Any] = dict(response_facets=response_facets.dict())
        if response_type is not None:
            response.update(response_type=response_type)

        super().__init__(**{**response, **kwargs})

    def with_card(
        self,
        card: CardFacet = None,
        *,
        icon_url: Text = None,
        title_text: Text = None,
        type_description: Text = None,
        image_url: Text = None,
        prominent_text: Text = None,
        action_prominent_text: Text = None,
        text: Text = None,
        sub_text: Text = None,
        media_url: Text = None,
        list_sections: List[ListSection] = None,
    ) -> "SkillInvokeResponse":
        """
        Attach Card to a response

        :param card:
        :param icon_url:
        :param title_text:
        :param type_description:
        :param image_url:
        :param prominent_text:
        :param action_prominent_text:
        :param text:
        :param sub_text:
        :param media_url:
        :param list_sections:
        :return:
        """
        return self.copy(
            update=dict(
                response_facets=self.response_facets.copy(
                    update=dict(
                        card=card or CardFacet(
                            icon_url=icon_url,
                            title_text=title_text,
                            type_description=type_description,
                            image_url=image_url,
                            prominent_text=prominent_text,
                            action_prominent_text=action_prominent_text,
                            text=text,
                            sub_text=sub_text,
                            media_url=media_url,
                            list_sections=list_sections,
                        )
                    )
                )
            )
        )

    def with_facets(
            self,
            *,
            command: Optional[Command] = None,
            task: Optional[ClientTask] = None,
            target_device_id: Optional[Text] = None,
            masked_response: Optional[Text] = None,
            ssml: Optional[Text] = None,
            card: Optional[CardFacet] = None
    ) -> "SkillInvokeResponse":

        facets: Dict[Text, Any] = {}
        if command is not None or task is not None:
            instructions = self.response_facets.touchpoint_instructions or TouchpointInstructionsFacet(data={})
            if command is not None:
                instructions.update(command.dict())
            if task is not None:
                instructions = instructions.with_task(task)
            facets.update(touchpoint_instructions=instructions)
        if target_device_id is not None:
            facets.update(event_history=EventHistoryFacet(target_device_id=target_device_id))
        if masked_response is not None:
            facets.update(vast=VastFacet(masked_response=masked_response))
        if ssml is not None:
            facets.update(tts=TtsFacet(ssml=ssml))
        if card is not None:
            facets.update(card=card)

        if len(facets) != 0:
            return self.copy(update=dict(response_facets=self.response_facets.copy(update=facets)))
        return self

    def with_command(self, command: Command) -> "SkillInvokeResponse":
        """
        Add a command to execute on the client

        :param command:
        :return:
        """
        touchpoint_instructions = TouchpointInstructionsFacet(data=command.dict())
        return self.copy(
            update=dict(
                response_facets=self.response_facets.copy(
                    update=dict(
                        touchpoint_instructions=touchpoint_instructions
                    )
                )
            )
        )

    def with_target_device_id(self, target_device_id: Text) -> "SkillInvokeResponse":
        return self.copy(
            update=dict(
                response_facets=self.response_facets.copy(
                    update=dict(
                        event_history=EventHistoryFacet(target_device_id=target_device_id)
                    )
                )
            )
        )

    def with_masked_response(self, masked_response: Text) -> "SkillInvokeResponse":
        return self.copy(
            update=dict(
                response_facets=self.response_facets.copy(
                    update=dict(
                        vast=VastFacet(masked_response=masked_response)
                    )
                )
            )
        )

    def with_ssml(self, ssml: Text) -> "SkillInvokeResponse":
        return self.copy(
            update=dict(
                response_facets=self.response_facets.copy(
                    update=dict(
                        tts=TtsFacet(ssml=ssml)
                    )
                )
            )
        )

    def with_session(self, **attributes) -> "SkillInvokeResponse":
        """
        Add attributes (key -> value) to keep in session storage

            (valid only for ResponseType.ASK/ASK_FREETEXT:
             ResponseType.TELL immediately ends the session)

        :param attributes:
        :return:
        """

        if self.response_type == ResponseType.TELL:
            raise ValueError(f"Response type: {self.response_type} ends the session.")

        session = SessionResponse(attributes=attributes)
        return self.copy(update=dict(session=session))

    def with_task(self, task: ClientTask):
        """
        Add a delayed client task

        :param task:
        :return:
        """
        touchpoint_instructions = self.response_facets.touchpoint_instructions or TouchpointInstructionsFacet(data={})
        return self.copy(
            update=dict(
                response_facets=self.response_facets.copy(
                    update=dict(
                        touchpoint_instructions=touchpoint_instructions.with_task(task)
                    )
                )
            )
        )


def _enrich(response: SkillInvokeResponse) -> SkillInvokeResponse:
    """
    Post-process a skill invoke response:

        - If simple text is returned - convert to Response
        - If session attributes are present - add to response

    :param response:
    :return:
    """
    from skill_sdk.intents.request import r

    if isinstance(response, str):
        # Convert string response to Response object
        response = SkillInvokeResponse(data=response)

    #
    # Copy session attributes from global request,
    # unless response is TELL, that ends the session
    #
    if response.response_type != ResponseType.TELL and r.session.attributes:
        attributes = copy.deepcopy(r.session.attributes)
        return response.with_session(**attributes)

    return response
