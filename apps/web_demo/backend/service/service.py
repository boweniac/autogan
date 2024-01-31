from typing import Dict, List, Optional

from autogan import UniversalAgent

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
            storage: Optional[StorageProtocol] = None,
            default_agent: Optional[UniversalAgent] = None,
    ):
        self._org_structure = org_structure
        self._switch = autogan.Switch(default_agent_config, org_structure, task_tag, consider_mode=super_rich,
                                      stream_mode=stream_mode, storage=storage, default_language="CN", default_agent=default_agent)

    async def a_receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                        response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator):
        conv_info = ConvHolder(conversation_id, task_id, response, snowflake_id_generator)
        conv_info.init_message(pusher_name, "HUMAN")
        conv_info.update_message(content)
        await response.a_send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", content, 0, None)
        await response.a_send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", "[DONE]", 0, None)

        await self._switch.a_handle_and_forward(conv_info)

    def receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator):
        conv_info = ConvHolder(conversation_id, task_id, response, snowflake_id_generator)
        conv_info.init_message(pusher_name, "HUMAN")
        conv_info.update_message(content)
        response.send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", content, 0, None)
        response.send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", "[DONE]", 0, None)

        self._switch.handle_and_forward(conv_info)
