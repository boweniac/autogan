import sys
from typing import Optional

from autogan.oai.count_tokens_utils import count_text_tokens

from autogan.agents.universal_agent import UniversalAgent
from enum import Enum

from autogan.oai.conv_holder import ConvHolder


class InputModel(Enum):
    API = "API"
    TERMINAL = "TERMINAL"


class HumanAgent(UniversalAgent):
    def __init__(
            self,
            name,
            duty: Optional[str] = None,
            model: Optional[InputModel] = InputModel.TERMINAL
    ):
        """Human agent

        Interact with other agents through forms.

        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        """
        super().__init__(
            name,
            duty=duty,
            agent_type="HUMAN"
        )
        self._model = model

    def new_task(self, conv_info: ConvHolder):
        if self._model == InputModel.TERMINAL:
            super().new_task(conv_info)

    async def a_new_task(self, conv_info: ConvHolder):
        if self._model == InputModel.TERMINAL:
            await super().a_new_task(conv_info)

    def receive(self, conv_info: ConvHolder):
        if self._model == InputModel.TERMINAL:
            super().receive(conv_info)

    async def a_receive(self, conv_info: ConvHolder):
        if self._model == InputModel.TERMINAL:
            await super().a_receive(conv_info)

    def tool_function(self, conversation_id: int, task_id: int, lang: Optional[str] = None, code: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int, str, str]:
        if self._model == InputModel.TERMINAL:
            try:
                reply = input("Please enter: ")
                if reply:
                    tokens = count_text_tokens(reply)
                    return reply, tokens, "", ""
                else:
                    sys.exit()
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                sys.exit()
