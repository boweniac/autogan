from typing import Protocol, Optional


class StorageProtocol(Protocol):
    """外部存储类，用于持久化存储会话数据，以便在服务重启或迁移后可衔接历史会话

    SQL表：
        agent_conversation：用于存储会话信息（不包括对话内容）
            - main_field：id, user_id, title
        agent_task：用于存储任务信息（不包括对话内容）
            - main_field：conversation_id, par_task_id, par_agent_name, par_agent_type, task_id, agent_name, agent_type, content
        agent_message：存储会话消息记录（完整会话消息，用于前端展示，不根据任务进行分割）
            - main_field：msg_id, conversation_id, task_id, content_type, content_tag, agent_name, content, tokens
        agent_task_message：缓存任务消息记录
            - main_field：id, task_id, role, name, tokens, content

    REDIS键：
        convs_list（哈希）：用于缓存用户会话列表（不包括对话内容）
            - key：用户 id
            - value：用户的会话列表
        convs_user_perms（哈希）：用户缓存会话鉴权信息
            - key：会话 id
            - value：用户 id
        task_get_par_id（哈希）：用于通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - key：下级任务id_上级 agent 名称
            - value：上级任务 id
        task_get_id（哈希）: 用于通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
            - key：上级任务id_下级 agent 名称
            - value：下级任务 id
        task_info（哈希）：用于缓存任务信息。
            - key：任务 id
            - value：上级 agent 名称, 上级 agent 类型, 任务内容
        conv_last_task_id（哈希）：用于缓存会话中 agent 执行的最后一个任务 id
            - key：会话 id_agent 名称
            - value：最后一个任务的 id
        conv_last_msg_id（哈希）：用于缓存会话最后一条消息 id 的缓存。
            - key：会话 id
            - value：最后一条消息的 id
        task_comp_messages（哈希）：用于缓存任务的消息记录
            - key：任务 id
            - value：消息列表
    """
    def add_task(self, conversation_id: int, par_task_id: int, par_agent_name: str, par_agent_type: str, task_id: int,
                 agent_name: str, agent_type: str, content: str):
        """添加任务
        SQL操作：
            - agent_task：插入新记录

        REDIS操作：
            - task_get_par_id：新增通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 新增通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
            - task_info：新增任务信息缓存。
            - conv_last_task_id：新增会话中 agent 执行的最后一个任务 id 的缓存。"""
        pass

    def get_task_info(self, task_id: int) -> Optional[dict]:
        """获取任务信息
        REDIS操作：
            - task_info：获取任务信息缓存

        失败后执行操作：
        SQL：
            - agent_conversation：查询符合特定 用户 id 值的所有记录

        REDIS：
            - task_get_par_id：新增通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 新增通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
            - task_info：新增任务信息缓存。"""
        pass

    def convert_main_or_sub_task_id(self, task_id: int, receiver_name: str) -> tuple[Optional[int], Optional[int]]:
        """转换任务 id：将下级任务 id 转换为上级任务 id，或是将上级任务 id 转换为下级任务 id
        REDIS操作：
            - task_get_par_id：通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。

        失败后执行操作：
        SQL：
            - agent_task：通过下级任务 di 和上级 agent 名称，查找上级任务 id。
            - agent_task: 通过上级任务 di 和下级 agent 名称，查找下级任务 id。

        REDIS：
            - task_get_par_id：新增通过下级任务 di 和上级 agent 名称，查找上级任务 id 的缓存。
            - task_get_id: 新增通过上级任务 di 和下级 agent 名称，查找下级任务 id 的缓存。
            - task_info：新增任务信息缓存。"""
        pass

    def get_conversation_latest_task(self, conversation_id: int, agent_name: str) -> Optional[int]:
        """获取会话中 agent 执行的最后一个任务 id
        REDIS操作：
            - conv_last_task_id：获取会话中 agent 执行的最后一个任务 id 的缓存。

        失败后执行操作：
        SQL：
            - agent_task：查询会话中 agent 执行的最后一个任务 id

        REDIS：
            - conv_last_task_id：缓存会话中 agent 执行的最后一个任务 id"""
        pass

    def add_message(self, conversation_id: int, message: dict) -> None:
        """添加会话消息记录（完整会话消息，用于前端展示，不根据任务进行分割）
        SQL操作：
            - agent_message：插入新记录

        REDIS操作：
            - conv_last_msg_id：新增会话最后一条消息 id 的缓存。"""
        pass

    def save_compressed_messages(self, task_id: int, messages: list) -> None:
        """缓存压缩后的任务消息记录
        REDIS操作：
            - task_comp_messages：缓存任务消息记录"""
        pass

    def add_compressed_message(self, task_id: int, message: dict) -> None:
        """添加任务消息记录
        SQL操作：
            - agent_task_message：插入新记录

        REDIS操作：
            - task_comp_messages：获取任务消息记录缓存
            - task_comp_messages：更新任务消息记录缓存"""
        pass

    def get_compressed_messages(self, task_id: int) -> Optional[list]:
        """获取任务消息记录
        REDIS操作：
            - task_comp_messages：获取任务消息记录缓存。

        失败后执行操作：
        SQL：
            - agent_task_message：查询任务的所有消息记录

        REDIS：
            - task_comp_messages：更新任务消息记录缓存"""
        pass
