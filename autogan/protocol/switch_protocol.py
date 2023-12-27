from typing import Protocol, Optional

from autogan.oai.config_utils import AgentConfig
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.protocol.storage_protocol import StorageProtocol

from autogan.utils.response import ResponseFuncType
from autogan.utils.uuid_utils import SnowflakeIdGenerator


class SwitchProtocol(Protocol):
    default_agent_config: AgentConfig
    task_tag: str
    snowflake_id: SnowflakeIdGenerator
    default_super_rich: Optional[str]
    default_stream_mode: Optional[bool]
    response: Optional[ResponseFuncType]
    storage: Optional[StorageProtocol]

    def handle_and_forward(self, conversation_id: int, task_id: int, pusher_name: str, content: str, response: ResponseProtocol,
                           completion_tokens: Optional[int], msg_id: Optional[int]) -> None:
        pass

    async def a_handle_and_forward(self, conversation_id: int, task_id: int, pusher_name: str, content: str, response: ResponseProtocol,
                                   completion_tokens: Optional[int], msg_id: Optional[int]) -> None:
        pass

    def system_prompt(self, conversation_id: int, task_id: int, receiver: str, content: str, response: ResponseProtocol) -> None:
        pass

    async def a_system_prompt(self, conversation_id: int, task_id: int, receiver: str, content: str, response: ResponseProtocol) -> None:
        pass
