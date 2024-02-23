from typing import Dict, List, Optional

from apps.web_demo.backend.db.db_storage import DBStorage
from autogan import UniversalAgent

import autogan
from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.protocol.storage_protocol import StorageProtocol
from autogan.oai.conv_holder import DialogueManager
from autogan.utils.es_utils import ESSearch
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
            es: Optional[ESSearch] = None,
            default_agent: Optional[UniversalAgent] = None,
    ):
        self._org_structure = org_structure
        self._switch = autogan.Switch(default_agent_config, org_structure, task_tag, consider_mode=super_rich,
                                      stream_mode=stream_mode, storage=storage, es=es, default_language="CN", default_agent=default_agent)

    async def a_receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                        response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator):
        conv_info = DialogueManager(conversation_id, response, snowflake_id_generator)
        conv_info.init_message_before_generate(pusher_name, "HUMAN")
        tokens = count_text_tokens(content)
        conv_info.before_switch(content, tokens)
        await response.a_send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", content, 0, None)
        await response.a_send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", "[DONE]", 0, None)

        await self._switch.a_handle_and_forward(conv_info)

    def receive(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                response: ResponseProtocol, snowflake_id_generator: SnowflakeIdGenerator):
        conv_info = DialogueManager(conversation_id, response, snowflake_id_generator)
        conv_info.init_message_before_generate(pusher_name, "HUMAN")
        tokens = count_text_tokens(content)
        conv_info.before_switch(content, tokens)
        response.send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", content, 0, None)
        response.send(conv_info.msg_id, task_id, pusher_name, 0, "main", "", "[DONE]", 0, None)

        self._switch.handle_and_forward(conv_info)

    def add_file_message(self, conv_info: DialogueManager):
        self._switch.default_agent.storage_add_compressed_message(conv_info)

    async def a_auto_title(self, storage: DBStorage, request_data: ChatCompletionsRequest, conv_info: DialogueManager, user_id: int, conversation_id: int):
        title, _ = await self._switch.a_auto_title(request_data, conv_info)
        storage.update_conversation_title(user_id, conversation_id, title)

    def auto_title(self, storage: DBStorage, request_data: ChatCompletionsRequest, conv_info: DialogueManager, user_id: int, conversation_id: int):
        title, _ = self._switch.auto_title(request_data, conv_info)
        storage.update_conversation_title(user_id, conversation_id, title)
