import re
import sys
from collections import defaultdict
from typing import List, Optional, Dict

from autogan.oai.count_tokens_utils import count_text_tokens

from autogan import UniversalAgent
from autogan.oai.config_utils import AgentConfig
from autogan.protocol.response_protocol import ResponseProtocol
from autogan.protocol.storage_protocol import StorageProtocol
from autogan.switch.default_response import DefaultResponse
from autogan.protocol.switch_protocol import SwitchProtocol
from autogan.utils.uuid_utils import SnowflakeIdGenerator


class Switch(SwitchProtocol):
    def __init__(
            self,
            default_agent_config: Dict,
            org_structure: List,
            task_tag: Optional[str] = "/task",
            opening_speaker: Optional[UniversalAgent] = None,
            super_rich: Optional[str] = None,
            stream_mode: Optional[bool] = None,
            storage: Optional[StorageProtocol] = None
    ):
        """All messages sent by agents need to be forwarded through the AgentSwitch object.
        所有 agent 发送的消息，都需要通过 AgentSwitch 对象进行转发。

        **Forwarding:**
        转发：

        The AgentSwitch object determines who to forward the message to based on the agent name after the @ symbol in the message.
        AgentSwitch 对象通过消息中 @ 符号后的 agent name 来判断将消息转发给谁。

        **Conversation domain:**
        会话域：

        In each round of dialogue, the agent does not need to use all historical conversation records as its context.
        每轮对话 agent 无需将所有的历史会话记录作为其上下文。

        The agent's conversation domain is based on the task. that is, the context of each round of dialogue for the agent only focuses on the historical conversation records of the current task.
        agent 的会话域以任务为基础。即 agent 每轮对话的上下文仅聚焦于当前任务的历史会话记录。

        **Task:**
        任务：

        The AgentSwitch object determines whether the content of the message is a task through the task tag in the message.
        AgentSwitch 对象通过消息中的 task tag，来判断消息的内容是否是一个任务。

        If it is a task, the AgentSwitch object will call the receiver's new_task method.
        如果是任务，AgentSwitch 对象会调用接收方的 new_task 方法。

        The default task tag is /task, which can be modified through the task_tag parameter when initializing the AgentSwitch object.
        task tag 默认为 /task，该值可在初始化 AgentSwitch 对象时，通过 task_tag 参数修改。

        **Organizational structure:**
        组织架构：

        A multidimensional list containing agent objects.
        一个包含 agent 对象的多维列表。

        Each list is equivalent to a department, and the first agent in the list is the leader of the department.
        每个列表相当于一个部门，列表中的第一个 agent 为部门的 leader。

        Each agent can communicate with other agents in the current department and the leader of the subordinate department to complete tasks together.
        每个 agent 可与当前部门的其他 agent 以及下级部门的 leader 沟通，协作完成任务。

        Note: There cannot be agents with the same name in the organizational structure.
        注意：组织架构中不能有相同名称的 agent。

        :param org_structure: A multidimensional list containing agent objects.
            一个包含 agent 对象的多维列表。
        :param opening_speaker: The name of the human agent invited to publish the first task.
            被邀请发布第一个任务的人工 agent 名称。
        :param task_tag: Publish tasks to other agents by adding task_tag to the message.
            通过在消息中添加 task_tag 来向其他 agent 发布任务。
        """
        self.task_tag = task_tag
        self.snowflake_id = SnowflakeIdGenerator(datacenter_id=1, worker_id=1)
        self.default_agent_config = AgentConfig(default_agent_config)
        self.default_super_rich = super_rich
        self.default_stream_mode = stream_mode
        self.storage = storage
        self._agents = defaultdict(UniversalAgent)  # key: agent name value: agent object
        self._init_agents(org_structure)
        self._init_agents_workmates(org_structure)
        if opening_speaker:
            self._inviting_to_speak(opening_speaker)

    def _init_agents(self, agent_list: list):
        for item in agent_list:
            if isinstance(item, list):
                self._init_agents(item)
            elif isinstance(item, str):
                continue
            elif isinstance(item, UniversalAgent):
                self._agents[item.name] = item
                item.switch = self
            else:
                raise ImportError("There are unknown type objects in the organizational structure.")

    def _init_agents_workmates(self, agent_list: list):
        """Arrange for each agent to communicate with other agents according to the organizational structure.
        根据组织架构，为每个 agent 安排可以与其沟通的其他 agent

        An agent should not exist in multiple departments.
        agent 不应存在于多个部门中

        :param agent_list: Organizational structure
            组织架构
        """
        if isinstance(agent_list[0], str):
            # The current list is workflow mode
            # 当前数组是工作流数组
            agent_list_len = len(agent_list)

            for index, main_item in enumerate(agent_list):
                workmates = ""

                # Skip the first element
                if index == 0:
                    continue

                # Get the next agent
                if isinstance(agent_list[index + 1], list):
                    agent = agent_list[index + 1][0]
                else:
                    agent = agent_list[index + 1]

                if not isinstance(agent, UniversalAgent):
                    raise ImportError("There are unknown type objects in the organizational structure.")

                if index == agent_list_len - 1:
                    # If this is the last element
                    name = "\\"
                else:
                    # If the next element is a list
                    name = agent.name
                    duty = agent.duty
                    workmates = f"""
{name} : {duty}"""

                # Get the current agent
                if isinstance(main_item, list):
                    # If the current element is a list
                    self._init_agents_workmates(main_item)
                    main_agent = main_item[0]
                else:
                    main_agent = main_item

                if not isinstance(main_agent, UniversalAgent):
                    continue

                if not agent.pipeline or agent.pipeline == "\\":
                    agent.workmates += workmates
                    agent.pipeline = name
        else:
            # The current list is non-workflow mode.
            # 当前数组是非工作流数组
            for main_item in agent_list:
                workmates = ""

                if isinstance(main_item, list):
                    self._init_agents_workmates(main_item)
                    main_agent = main_item[0]
                else:
                    main_agent = main_item

                if not isinstance(main_agent, UniversalAgent):
                    continue

                for item in agent_list:
                    # Establish a leveling relationship between current department leaders
                    if isinstance(item, list):
                        # If other elements are lists
                        if isinstance(item[0], str):
                            if item[0] == "F":
                                # If it is a workflow
                                if isinstance(item[1], list):
                                    agent = item[1][0]
                                else:
                                    agent = item[1]
                            else:
                                continue
                        else:
                            agent = item[0]
                            if agent.name == main_agent.name:
                                continue
                    else:
                        agent = item

                    if not isinstance(agent, UniversalAgent):
                        raise ImportError("There are unknown type objects in the organizational structure.")

                    if agent.name == main_agent.name:
                        continue

                    name = agent.name
                    duty = agent.duty
                    workmates += f"""
{name} : {duty}"""
                main_agent.workmates += workmates

    def _inviting_to_speak(self, invited_speaker: UniversalAgent):
        """Invite the human agent to publish the first task
        邀请人工 agent 发布第一个任务

        :param invited_speaker: The name of the human agent
            人工 agent 名称。
        """
        if invited_speaker.name not in self._agents:
            print("agent does not exist")
            return
        new_task_id = self.snowflake_id.next_id()
        response_proxy = DefaultResponse()
        invited_speaker.receive(new_task_id, new_task_id, "system", "Please enter", 2, response_proxy)

    def handle_and_forward(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                           response_proxy: ResponseProtocol, completion_tokens: Optional[int], msg_id: Optional[int]) -> None:
        handle_dict = self.handle(conversation_id, task_id, pusher_name, content, completion_tokens, msg_id, response_proxy)

        if handle_dict:
            if handle_dict["type"] == "system":
                self.system_prompt(conversation_id, handle_dict["switch_task_id"], handle_dict["receiver_name"],
                                   handle_dict["content"],
                                   response_proxy)
            elif handle_dict["type"] == "new_task":
                handle_dict["receiver"].new_task(conversation_id, handle_dict["switch_task_id"],
                                                 handle_dict["sender_name"],
                                                 handle_dict["content"], handle_dict["tokens"], response_proxy)
            else:
                handle_dict["receiver"].receive(conversation_id, handle_dict["switch_task_id"],
                                                handle_dict["sender_name"],
                                                handle_dict["content"], handle_dict["tokens"], response_proxy)

    async def a_handle_and_forward(self, conversation_id: int, task_id: int, pusher_name: str, content: str,
                                   response_proxy: ResponseProtocol,
                                   completion_tokens: Optional[int], msg_id: Optional[int]) -> None:
        handle_dict = self.handle(conversation_id, task_id, pusher_name, content, completion_tokens, msg_id, response_proxy)

        if handle_dict:
            if handle_dict["type"] == "system":
                await self.a_system_prompt(conversation_id, handle_dict["switch_task_id"], handle_dict["receiver_name"],
                                           handle_dict["content"],
                                           response_proxy)
            elif handle_dict["type"] == "new_task":
                await handle_dict["receiver"].a_new_task(conversation_id, handle_dict["switch_task_id"],
                                                         handle_dict["sender_name"],
                                                         handle_dict["content"], handle_dict["tokens"], response_proxy)
            else:
                await handle_dict["receiver"].a_receive(conversation_id, handle_dict["switch_task_id"],
                                                        handle_dict["sender_name"],
                                                        handle_dict["content"], handle_dict["tokens"], response_proxy)

    def handle(self, conversation_id: int, task_id: int, pusher_name: str, content: str, completion_tokens: Optional[int], msg_id: Optional[int], response_proxy: ResponseProtocol) \
            -> Optional[Dict]:
        """Handle messages and forward to other agent.
        处理消息并转发给其他代理

        **Forwarding:**
        转发：
        Determines who to forward the message to based on the agent name after the @ symbol in the message.
        通过消息中 @ 符号后的 agent name 来判断将消息转发给谁。

        **Task:**
        任务：
        Determines whether the content of the message is a task through the task tag in the message.
        通过消息中的 task tag，来判断消息的内容是否是一个任务。

        If it is a task, will call the receiver's new_task method.
        如果是任务，对象会调用接收方的 new_task 方法。

        **Conversation domain control:**
        会话域控制：
        Translate the task id of the pusher into the task id of the receiver to connect the context.
        将推送方的任务 id，转换为接收方的任务 id，以衔接上下文。

        - If the pusher is the task publisher, it is necessary to convert the task id of the pusher into the sub-task id of the receiver.
        - 如推送方为任务发布者，则需要将推送方的任务 id 转换为接收方的子任务 id。

        - If the pusher is executing the task published by the receiver, it is necessary to convert the task id of the pusher into the parent task id of the receiver.
        - 如推送方正在执行接收方发布的任务，则需要将推送方的任务 id 转换为接收方的上级任务 id。

        :param task_id: pusher task id.
        :param pusher_name: pusher_name.
        :param content: message content.
        :param completion_tokens: message content tokens.
        """
        # Get pusher object.
        pusher = self._agents[pusher_name]

        # Recognize the recipient's name.
        match = re.findall(r'@(\w+)', content)

        self.storage and self.storage.add_message(conversation_id, {"id": msg_id, "task_id": task_id, "agent_name": pusher_name, "content": content, "tokens": completion_tokens})

        if match:
            if match[0] not in self._agents:
                # Handling the case of incorrect recipient name.
                response_type = "system"
                receiver = pusher
                current_task_id = task_id
                switch_task_id = task_id
                sender_name = "system"
                content = f"@{pusher_name} {match[0]} not exist, do not @{match[0]} again, Also please do not attempt to converse with me, this is just a system message."
                completion_tokens = 30
            elif re.search(fr'@\w+ {self.task_tag}', content):
                response_type = "new_task"
                receiver = self._agents[match[0]]
                current_task_id = task_id
                switch_task_id = self.snowflake_id.next_id()
                sender_name = pusher_name

                # Establish a relationship between the push task and the receiver task.
                pusher.save_sub_to_main_task_id(switch_task_id, task_id)
                receiver.save_main_to_sub_task_id(task_id, switch_task_id)
            else:
                receiver = self._agents[match[0]]
                sender_name = pusher_name
                current_task_id = task_id
                switch_task_id = task_id
                sub_task_id = receiver.convert_main_to_sub_task_id(task_id)
                if sub_task_id:
                    # Translate the session ID of the pusher into the sub-session ID of the receiver.
                    switch_task_id = sub_task_id
                main_task_id = receiver.convert_sub_to_main_task_id(task_id)
                if main_task_id:
                    # Translate the session id of the sender into the superior session id of the receiver.
                    switch_task_id = main_task_id
                if switch_task_id == task_id:
                    # If no subtasks of the task from the pusher are found, a prompt is needed to create the task first.
                    response_type = "new_task"
                    switch_task_id = self.snowflake_id.next_id()

                    # Establish a relationship between the push task and the receiver task.
                    pusher.save_sub_to_main_task_id(switch_task_id, task_id)
                    receiver.save_main_to_sub_task_id(task_id, switch_task_id)
                    # Create a new task.
                    content = content.replace(f"@{match[0]} ", f"@{match[0]} {self.task_tag} ")
                else:
                    response_type = "general"
        else:
            # Handling the situation where the recipient is not recognized.
            if pusher.pipeline != "\\":
                response_type = "system"
                receiver = pusher
                current_task_id = task_id
                switch_task_id = task_id
                sender_name = "system"
                content = f"@{pusher_name} Any reply must start with @ + recipient's name, Also please do not attempt to converse with me, this is just a system message."
                completion_tokens = 30
            else:
                return

        max_conv_turns = self.default_agent_config.main_model_config.max_conv_turns
        if (max_conv_turns and max_conv_turns >= response_proxy.conv_turns) or not response_proxy.need_to_stop():
            response_proxy.conv_turns += 1
            return {"type": response_type, "receiver": receiver, "receiver_name": receiver.name,
                    "current_task_id": current_task_id, "switch_task_id": switch_task_id,
                    "sender_name": sender_name, "content": content, "tokens": completion_tokens}
        else:
            return

    def system_prompt(self, conversation_id: int, task_id: int, receiver_name: str, content: str,
                      response_proxy: ResponseProtocol) -> None:
        msg_id = self.snowflake_id.next_id()
        content = f"@{receiver_name} {content}"
        tokens = count_text_tokens(content)
        self.storage and self.storage.add_message(conversation_id, {"id": msg_id, "task_id": task_id, "agent_name": "system", "content": content, "tokens": tokens})
        response_proxy.send("system", "system", "", False, 1, content, tokens, None, msg_id, task_id)
        self._agents[receiver_name].receive(conversation_id, task_id, "system", content, tokens, response_proxy)

    async def a_system_prompt(self, conversation_id: int, task_id: int, receiver_name: str, content: str,
                              response_proxy: ResponseProtocol) -> None:
        msg_id = self.snowflake_id.next_id()
        content = f"@{receiver_name} {content}"
        tokens = count_text_tokens(content)
        self.storage and self.storage.add_message(conversation_id, {"id": msg_id, "task_id": task_id, "agent_name": "system", "content": content, "tokens": tokens})
        await response_proxy.a_send("system", "system", "", False, 1, content, tokens, None, msg_id, task_id)
        await self._agents[receiver_name].a_receive(conversation_id, task_id, "system", content, tokens, response_proxy)

