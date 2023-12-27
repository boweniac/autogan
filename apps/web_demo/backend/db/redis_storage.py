import json
from typing import Optional

import redis

from autogan.protocol.storage_protocol import StorageProtocol


class RedisStorage(StorageProtocol):
    def __init__(
            self,
            host: str,
            port: int,
            db: Optional[int] = 0
    ):
        self._redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def add_conversation(self, user_id: int, conversation_id: int) -> Optional[str]:
        existing_user_id = self._redis.hget('conv_user_map', str(conversation_id))
        if existing_user_id:
            if int(existing_user_id) == user_id:
                return "The conversation already exists."
            else:
                return "Conversation permission error."
        else:
            self._redis.hset('conv_user_map', str(conversation_id), str(user_id))
            return None

    def user_conversation_permissions(self, user_id: int, conversation_id: int) -> bool:
        existing_user_id = self._redis.hget('conv_user_map', str(conversation_id))
        if existing_user_id:
            if int(existing_user_id) == user_id:
                return True
            else:
                return False
        else:
            return False

    def save_task_info(self, task_id: int, task_info: dict) -> None:
        self._redis.hset('task_info', str(task_id), json.dumps(task_info))

    def get_task_info(self, task_id: int) -> Optional[dict]:
        data_dict = self._redis.hget(f'task_info', str(task_id))
        if data_dict:
            return json.loads(data_dict)
        else:
            return None

    def save_main_to_sub_task_id(self, main_task_id: int, sub_task_id: int) -> None:
        self._redis.hset('main_to_sub_task_id', str(main_task_id), str(sub_task_id))

    def save_sub_to_main_task_id(self, main_task_id: int, sub_task_id: int) -> None:
        self._redis.hset('sub_to_main_task_id', str(sub_task_id), str(main_task_id))

    def convert_main_to_sub_task_id(self, task_id: int) -> Optional[int]:
        task_id = self._redis.hget(f'main_to_sub_task_id', str(task_id))
        if task_id:
            return int(task_id)
        else:
            return None

    def convert_sub_to_main_task_id(self, task_id: int) -> Optional[int]:
        task_id = self._redis.hget(f'sub_to_main_task_id', str(task_id))
        if task_id:
            return int(task_id)
        else:
            return None

    def add_message(self, conversation_id: int, message: dict) -> None:
        self._redis.rpush(f'conv_messages_{conversation_id}', json.dumps(message))
        self._redis.hset('conv_last_msg_id', str(conversation_id), message["id"])

    def get_last_msg_id(self, conversation_id: int) -> Optional[int]:
        last_msg_id = self._redis.hget('conv_last_msg_id', str(conversation_id))
        if last_msg_id:
            return int(last_msg_id)
        else:
            return None

    def get_messages(self, conversation_id: int) -> Optional[list]:
        return self._redis.lrange(f'conv_messages_{conversation_id}', 0, -1)

    def save_compressed_messages(self, task_id: int, messages: list) -> None:
        self._redis.hset('task_comp_messages', str(task_id), json.dumps(messages))

    def add_compressed_message(self, task_id: int, message: dict) -> None:
        messages = self._redis.hget(f'task_comp_messages', str(task_id))
        if messages:
            decoded = json.loads(messages)
            decoded.append(message)
            self._redis.hset('task_comp_messages', str(task_id), json.dumps(decoded))
        else:
            self._redis.hset('task_comp_messages', str(task_id), json.dumps([message]))

    def get_compressed_messages(self, task_id: int) -> Optional[list]:
        messages = self._redis.hget(f'task_comp_messages', str(task_id))
        if messages:
            return json.loads(messages)
        else:
            return None
