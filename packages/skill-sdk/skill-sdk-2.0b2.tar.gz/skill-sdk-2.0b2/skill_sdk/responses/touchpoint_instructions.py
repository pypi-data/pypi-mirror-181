#
#
# voice-skill-sdk
#
# (C) 2021, Deutsche Telekom AG
#
# This file is distributed under the terms of the MIT license.
# For details see the file LICENSE in the top directory.
#

"""Skill invoke data response"""

from typing import Dict, Optional
from skill_sdk.utils.util import CamelModel
from skill_sdk.responses.task import DelayedClientTask


class TouchpointInstructionsFacet(CamelModel):
    """Skill result in machine-readable format"""

    class Config:
        """This model instances are mutable for backward compatibility"""

        allow_mutation = True

    # Result data
    data: Dict

    # True if passed over to the local client
    local: Optional[bool]

    # Delayed client task
    delayed_client_task: Optional[DelayedClientTask]

    def __init__(
        self,
        data: Dict,
        *,
        local: Optional[bool] = None,
        delayed_client_task: Optional[DelayedClientTask] = None,
    ) -> None:
        """
        Rewrite positional arguments to keyword ones for backward compatibility

        :param data:
        :param local:
        :param delayed_client_task:
        """
        super().__init__(
            data=data,
            local=local,
            delayed_client_task=delayed_client_task,
        )

    def __getitem__(self, *args):
        return self.data.__getitem__(*args)

    def __bool__(self):
        return any((self.data, self.delayed_client_task))

    def update(self, *args, **kwargs):
        """
        Update `data`

        :return:
        """
        return self.data.update(*args, **kwargs)

    def with_task(self, task: DelayedClientTask):
        """
        Add task to result

        :param task:
        :return:
        """
        return self.copy(update=dict(delayed_client_task=task))
