from enum import Enum
from typing import Protocol, Optional

from autogan.protocol.response_protocol import ResponseProtocol

from autogan.oai.chat_config_utils import AgentConfig
from autogan.protocol.storage_protocol import StorageProtocol
from autogan.oai.conv_holder import ConvHolder
from autogan.utils.es_utils import ESSearch
from autogan.utils.uuid_utils import SnowflakeIdGenerator


# class Language(Enum):
#     EN = "EN"
#     CN = "CN"


class SwitchProtocol(Protocol):
    default_agent_config: AgentConfig
    task_tag: str
    default_consider_mode: Optional[str]
    default_stream_mode: Optional[bool]
    storage: Optional[StorageProtocol]
    es: Optional[ESSearch]
    default_language: str
    # default_agent_name: str

    def default_agent_name(self) -> Optional[str]:
        pass

    def handle_and_forward(self, conv_info: ConvHolder, content_type: Optional[str] = "main", content_tag: Optional[str] = "") -> None:
        pass

    async def a_handle_and_forward(self, conv_info: ConvHolder, content_type: Optional[str] = "main", content_tag: Optional[str] = "") -> None:
        pass

    def auto_title(self, user_id: int, conversation_id: int, response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator) -> None:
        pass

    async def a_auto_title(self, user_id: int, conversation_id: int, response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator) -> None:
        pass

    def system_alert(self, conv_info: ConvHolder) -> None:
        pass

    async def a_system_alert(self, conv_info: ConvHolder) -> None:
        pass
