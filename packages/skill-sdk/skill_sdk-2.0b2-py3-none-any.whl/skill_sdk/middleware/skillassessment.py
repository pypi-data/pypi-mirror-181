from enum import Enum
from typing import Callable, List, Dict, Optional, Text

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import Field

from skill_sdk.__version__ import __spi_version__
from skill_sdk.intents import AttributeV2, Session
from skill_sdk.utils.util import CamelModel, DEFAULT_LOCALE


class SkillFitnessInitiateJudgement(CamelModel):
    intent: Text
    skill_id: Text
    attributes: Dict[Text, List[AttributeV2]]
    svh_access_token: Text
    locale: Text = Field(example=DEFAULT_LOCALE)
    client_type_name: Optional[Text]
    session: Session
    spi_version: Text = Field(example=__spi_version__)


class SkillFitContentMap(CamelModel):
    skillFitConfidence: float


class SkillAssessmentResultType(Text, Enum):
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    CONNECTION_FAILED = "CONNECTION_FAILED"
    TIMEOUT = "TIMEOUT"
    OK = "OK"


class SkillFitAssessmentObject(CamelModel):
    result_type: SkillAssessmentResultType
    content_version: str
    content_map: Dict[str, str]


class SkillFitAssessmentSingleton(object):
    _instance = None
    _skill_fit_assess_func: Callable

    def __init__(self):
        if SkillFitAssessmentSingleton._instance is None:
            raise RuntimeError('Call SkillFitAssessmentSingleton.instance() instead')
        else:
            SkillFitAssessmentSingleton._instance = self

    def set_response_implementation(self, func_name):
        self._skill_fit_assess_func = func_name

    def get_response_implementation(self, r: SkillFitnessInitiateJudgement):
        response_object = self._skill_fit_assess_func(r)
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=dict(resultType=response_object.result_type,
                                         contentMap=jsonable_encoder(response_object.content_map),
                                         contentVersion=response_object.content_version))

    def return_default_response_implementation(self, r: SkillFitnessInitiateJudgement):
        return SkillFitAssessmentObject(result_type=SkillAssessmentResultType.NOT_IMPLEMENTED, content_version=1.0,
                                        content_map=dict(SkillFitContentMap(skillFitConfidence=0.0)))

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls._skill_fit_assess_func = cls.return_default_response_implementation

        return cls._instance
