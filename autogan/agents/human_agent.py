import sys
from typing import Optional

from autogan.protocol.response_protocol import ResponseProtocol

from autogan.oai.count_tokens_utils import count_text_tokens

from autogan.agents.universal_agent import UniversalAgent, ToolFunctionUsage
from enum import Enum


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
            tool_function_usage=ToolFunctionUsage.ONLY
        )
        self._model = model

    def new_task(self, conversation_id: int, task_id: int, sender_name: str, content: str, completion_tokens: int,
                 response_proxy: ResponseProtocol):
        if self._model == InputModel.TERMINAL:
            super().new_task(conversation_id, task_id, sender_name, content, completion_tokens, response_proxy)

    async def a_new_task(self, conversation_id: int, task_id: int, sender_name: str, content: str,
                         completion_tokens: int, response_proxy: ResponseProtocol):
        if self._model == InputModel.TERMINAL:
            await super().a_new_task(conversation_id, task_id, sender_name, content, completion_tokens, response_proxy)

    def receive(self, conversation_id: int, task_id: int, sender_name: str, content: str, completion_tokens: int,
                response_proxy: ResponseProtocol):
        if self._model == InputModel.TERMINAL:
            super().receive(conversation_id, task_id, sender_name, content, completion_tokens, response_proxy)

    async def a_receive(self, conversation_id: int, task_id: int, sender_name: str, content: str, completion_tokens: int,
                response_proxy: ResponseProtocol):
        if self._model == InputModel.TERMINAL:
            await super().a_receive(conversation_id, task_id, sender_name, content, completion_tokens, response_proxy)

    def tool_function(self, task_id: int, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        if self._model == InputModel.TERMINAL:
            try:
                reply = input("Please enter: ")
                if reply:
                    tokens = count_text_tokens(reply)
                    return reply, tokens
                else:
                    sys.exit()
            except KeyboardInterrupt:
                sys.exit()
            except Exception as e:
                sys.exit()

