from enum import Enum
from typing import Protocol, Optional

from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.protocol.response_protocol import ResponseProtocol

from autogan.oai.chat_config_utils import AgentLLMConfig
from autogan.protocol.storage_protocol import StorageProtocol
from autogan.oai.conv_holder import DialogueManager
from autogan.utils.es_utils import ESSearch
from autogan.utils.uuid_utils import SnowflakeIdGenerator


# class Language(Enum):
#     EN = "EN"
#     CN = "CN"


class SwitchProtocol(Protocol):
    default_agent_config: AgentLLMConfig
    task_tag: str
    default_consider_mode: Optional[str]
    default_stream_mode: Optional[bool]
    storage: Optional[StorageProtocol]
    es: Optional[ESSearch]
    default_language: str

    def handle_and_forward(self, conv_info: DialogueManager, content_type: Optional[str] = "main", content_tag: Optional[str] = "") -> None:
        pass

    async def a_handle_and_forward(self, conv_info: DialogueManager, content_type: Optional[str] = "main", content_tag: Optional[str] = "") -> None:
        pass

    def auto_title(self, request_data: ChatCompletionsRequest, conv_info: DialogueManager) -> tuple[str, int]:
        pass

    async def a_auto_title(self, request_data: ChatCompletionsRequest, conv_info: DialogueManager) -> tuple[str, int]:
        pass

    def system_alert(self, conv_info: DialogueManager) -> None:
        pass

    async def a_system_alert(self, conv_info: DialogueManager) -> None:
        pass
