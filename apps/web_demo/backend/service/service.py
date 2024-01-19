from typing import Dict, List, Optional

import autogan
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.protocol.storage_protocol import StorageProtocol
from autogan.oai.conv_holder import ConvHolder
from autogan.utils.uuid_utils import SnowflakeIdGenerator


class UniversalService:
    def __init__(
            self,
            default_agent_config: Dict,
            org_structure: List,
            task_tag: Optional[str] = "/task",
            super_rich: Optional[str] = None,
            stream_mode: Optional[bool] = None,
            storage: Optional[StorageProtocol] = None
    ):
        self._org_structure = org_structure
        self._switch = autogan.Switch(default_agent_config, org_structure, task_tag, consider_mode=super_rich,
                                      stream_mode=stream_mode, storage=storage)

    async def a_receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                        response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator):
        conv_info = ConvHolder(conversation_id, task_id, response, snowflake_id_generator)
        conv_info.init_message(pusher_name, "HUMAN")
        conv_info.update_message(content)
        await self._switch.a_handle_and_forward(conv_info)

    def receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator):
        conv_info = ConvHolder(conversation_id, task_id, response, snowflake_id_generator)
        conv_info.init_message(pusher_name, "HUMAN")
        conv_info.update_message(content)
        self._switch.handle_and_forward(conv_info)
