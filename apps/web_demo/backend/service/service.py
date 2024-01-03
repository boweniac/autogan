from typing import Dict, List, Optional

import autogan
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.protocol.storage_protocol import StorageProtocol


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
        self._switch = autogan.Switch(default_agent_config, org_structure, task_tag, super_rich=super_rich,
                                      stream_mode=stream_mode, storage=storage)

    async def a_receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str, response: ResponseProtocol):
        req_msg_id = self._switch.snowflake_id.next_id()
        # response.req_msg_id = req_msg_id
        await response.a_send(self._org_structure[0].name, "user", "", False, 0, content, None, None, req_msg_id, task_id)
        await self._switch.a_handle_and_forward(conversation_id, task_id, pusher_name, content, response, 0, req_msg_id)

    def receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str, response: ResponseProtocol):
        req_msg_id = self._switch.snowflake_id.next_id()
        # response.req_msg_id = req_msg_id
        response.send(self._org_structure[0].name, "main", "", False, 0, content, None, None, req_msg_id, task_id)
        self._switch.handle_and_forward(conversation_id, task_id, pusher_name, content, response, 0, req_msg_id)
