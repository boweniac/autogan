from typing import Protocol, Optional


class StorageProtocol(Protocol):
    def add_task(self, conversation_id: int, par_task_id: int, par_agent_name: str, par_agent_type: str, task_id: int,
                 agent_name: str, agent_type: str, content: str):
        pass

    # def save_task_info(self, task_id: int, task_info: dict) -> None:
    #     pass

    def get_task_info(self, task_id: int) -> Optional[dict]:
        pass

    # def save_main_to_sub_task_id(self, main_task_id: int, sub_task_id: int) -> None:
    #     pass

    # def save_sub_to_main_task_id(self, main_task_id: int, sub_task_id: int) -> None:
    #     pass

    def convert_main_or_sub_task_id(self, task_id: int, receiver_name: str) -> tuple[Optional[int], Optional[int]]:
        pass

    # def convert_main_to_sub_task_id(self, task_id: int) -> Optional[int]:
    #     pass

    # def convert_sub_to_main_task_id(self, task_id: int) -> Optional[int]:
    #     pass

    def get_conversation_latest_task(self, conversation_id: int, agent_name: str) -> Optional[int]:
        pass

    def add_message(self, conversation_id: int, message: dict) -> None:
        pass

    def get_last_msg_id(self, conversation_id: int) -> Optional[int]:
        pass

    def get_messages_when_changed(self, conversation_id: int, last_msg_id: int) -> Optional[list]:
        pass

    def get_messages(self, conversation_id: int) -> Optional[list]:
        pass

    def save_compressed_messages(self, task_id: int, messages: list) -> None:
        pass

    def add_compressed_message(self, task_id: int, message: dict) -> None:
        pass

    def get_compressed_messages(self, task_id: int) -> Optional[list]:
        pass

    # def save_conversation_latest_task(self, conversation_id: int, agent_name: str, task_id: int) -> None:
    #     pass

    def update_conversation_title(self, user_id: int, conversation_id: int, title: str):
        pass
