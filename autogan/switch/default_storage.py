import json
from collections import defaultdict
from typing import Optional
import redis

import autogan
import mysql.connector
from mysql.connector import Error
from DBUtils.PooledDB import PooledDB

from autogan.protocol.storage_protocol import StorageProtocol


class DefaultStorage(StorageProtocol):
    def __init__(self):
        """用于存储会话数据（非持久化存储，服务器重启数据会被清除）"""
        self._task_get_par_id = defaultdict(int)
        self._task_get_id = defaultdict(int)
        self._task_info = defaultdict(dict)
        self._conv_last_task_id = defaultdict(int)
        self._task_comp_messages = defaultdict(list)
        # self._conv_last_msg_id = defaultdict(int)

    def add_task(self, conversation_id: int, par_task_id: int, par_agent_name: str, par_agent_type: str, task_id: int,
                 agent_name: str, agent_type: str, content: str):
        """添加任务

        - task_get_par_id：新增通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
        - task_get_id: 新增通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
        - task_info：新增任务信息缓存。
        - conv_last_task_id：新增会话中 agent 执行的最后一个任务 id 的缓存。"""
        self._task_get_par_id[f"{task_id}_{par_agent_name}"] = par_task_id
        self._task_get_id[f"{par_task_id}_{agent_name}"] = task_id
        self._task_info[str(task_id)] = {"par_agent_name": par_agent_name, "par_agent_type": par_agent_type, "content": content}
        self._conv_last_task_id[f"{conversation_id}_{agent_name}"] = task_id

    def get_task_info(self, task_id: int) -> Optional[dict]:
        """获取任务信息

        - task_info：获取任务信息缓存"""
        return self._task_info[str(task_id)]

    def convert_main_or_sub_task_id(self, task_id: int, receiver_name: str) -> tuple[Optional[int], Optional[int]]:
        """转换任务 id：将下级任务 id 转换为上级任务 id，或是将上级任务 id 转换为下级任务 id

        - task_get_par_id：通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
        - task_get_id: 通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。"""
        par_task_id = self._task_get_par_id[f"{task_id}_{receiver_name}"]
        task_id = self._task_get_id[f"{task_id}_{receiver_name}"]

        return par_task_id, task_id

    def get_conversation_latest_task(self, conversation_id: int, agent_name: str) -> Optional[int]:
        """获取会话中 agent 执行的最后一个任务 id

        - conv_last_task_id：获取会话中 agent 执行的最后一个任务 id 的缓存。"""
        return self._conv_last_task_id[f"{conversation_id}_{agent_name}"]

    def add_message(self, conversation_id: int, message: dict) -> None:
        pass

    def save_compressed_messages(self, task_id: int, messages: list) -> None:
        """缓存压缩后的任务消息记录
        - task_comp_messages：缓存任务消息记录"""
        self._task_comp_messages[str(task_id)] = messages

    def add_compressed_message(self, task_id: int, message: dict) -> None:
        """添加任务消息记录
        - task_comp_messages：插入新记录"""
        self._task_comp_messages[str(task_id)].append(message)

    def get_compressed_messages(self, task_id: int) -> Optional[list]:
        """获取任务消息记录
        - task_comp_messages：获取任务消息记录缓存。"""
        return self._task_comp_messages[str(task_id)]
