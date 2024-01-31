import re
from collections import defaultdict
from typing import List, Optional, Dict

from autogan import UniversalAgent
from autogan.oai.chat_config_utils import AgentConfig
from autogan.protocol.storage_protocol import StorageProtocol
from autogan.oai.conv_holder import ConvHolder
from autogan.switch.default_response import DefaultResponse
from autogan.protocol.switch_protocol import SwitchProtocol
from autogan.utils.uuid_utils import SnowflakeIdGenerator


class Switch(SwitchProtocol):
    def __init__(
            self,
            default_agent_config: Dict,
            org_structure: List,
            task_tag: Optional[str] = None,
            invited_speakers: Optional[UniversalAgent] = None,
            consider_mode: Optional[str] = None,
            stream_mode: Optional[bool] = None,
            storage: Optional[StorageProtocol] = None,
            default_language: Optional[str] = None,
            default_agent: Optional[UniversalAgent] = None,
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
        :param default_agent_config: 默认 agent LLM 配置
        :param org_structure: 组织架构，一个包含 agent 对象的多维列表。
        :param task_tag: 任务关键词用于创建任务，默认值为 /task，例如 @客户经理 /task
        :param invited_speakers: 被邀请发布第一个任务的人工 agent 名称。
        :param consider_mode: 是否开启深思模式，默认值为 auto。
        :param stream_mode: 默认值为 True。
        :param storage: 存储对象，可根据需要自行实现会话记录的持久化存储
        """
        self.task_tag = task_tag if task_tag else "/task"
        self.default_language = "EN" if default_language is None else default_language
        self.default_agent_config = AgentConfig(default_agent_config)
        self._agents = defaultdict(UniversalAgent)  # key: agent name value: agent object
        self._init_agents(org_structure)
        self._init_agents_workmates(org_structure)
        if invited_speakers:
            self._inviting_to_speak(invited_speakers)
        self.default_consider_mode = consider_mode if consider_mode else "auto"
        self.default_stream_mode = stream_mode if stream_mode else True
        self.storage = storage
        self.default_agent = default_agent

    @property
    def default_agent_name(self) -> Optional[str]:
        if self.default_agent:
            return self.default_agent.name
        else:
            return None

    def _init_agents(self, org_structure: list):
        """注册组织架构中的所有 agent"""
        for item in org_structure:
            if isinstance(item, list):
                self._init_agents(item)
            elif isinstance(item, str):
                continue
            elif isinstance(item, UniversalAgent):
                self._agents[item.name] = item
                item.switch = self
            else:
                raise ImportError("There are unknown type objects in the organizational structure.")

    def _init_agents_workmates(self, org_structure: list):
        """Arrange for each agent to communicate with other agents according to the organizational structure.
        根据组织架构，为每个 agent 安排可以与其沟通的其他 agent

        An agent should not exist in multiple departments.
        agent 不应存在于多个部门中

        :param org_structure: Organizational structure
            组织架构
        """
        if isinstance(org_structure[0], str):
            # The current list is workflow mode
            # 当前数组是工作流数组
            agent_list_len = len(org_structure)

            for index, main_item in enumerate(org_structure):
                workmates = ""

                # Skip the first element
                if index == 0:
                    continue

                # Get the next agent
                if isinstance(org_structure[index + 1], list):
                    agent = org_structure[index + 1][0]
                else:
                    agent = org_structure[index + 1]

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
                    agent.init_prompts(self.default_language, self.task_tag, workmates, name)
        else:
            # The current list is non-workflow mode.
            # 当前数组是非工作流数组
            for main_item in org_structure:
                workmates = ""

                if isinstance(main_item, list):
                    self._init_agents_workmates(main_item)
                    main_agent = main_item[0]
                else:
                    main_agent = main_item

                if not isinstance(main_agent, UniversalAgent):
                    continue

                for item in org_structure:
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
                main_agent.init_prompts(self.default_language, self.task_tag, workmates, "")

    def _inviting_to_speak(self, invited_speaker: UniversalAgent):
        """Invite the human agent to publish the first task
        邀请人工 agent 发布第一个任务

        :param invited_speaker: The name of the human agent
            人工 agent 名称。
        """
        if invited_speaker.name not in self._agents:
            print("agent does not exist")
            return
        snowflake_id = SnowflakeIdGenerator(datacenter_id=1, worker_id=1)
        conversation_id = snowflake_id.next_id()
        response_proxy = DefaultResponse()

        conv_info = ConvHolder(conversation_id, conversation_id, response_proxy, snowflake_id)
        conv_info.init_message("system")
        conv_info.switch_to_agent(conversation_id, f"@{invited_speaker.name} Please enter: ")
        invited_speaker.receive(conv_info)

    def handle_and_forward(self, conv_info: ConvHolder) -> None:
        handle_dict = self.handle(conv_info)
        if handle_dict:
            if handle_dict["type"] == "system":
                conv_info.to_system_alert(handle_dict["content"])
                self.system_alert(conv_info)
            elif handle_dict["type"] == "new_task":
                conv_info.switch_to_agent(handle_dict["switch_task_id"], handle_dict["content"])
                handle_dict["receiver"].new_task(conv_info)
            else:
                conv_info.switch_to_agent(handle_dict["switch_task_id"], handle_dict["content"])
                handle_dict["receiver"].receive(conv_info)

    async def a_handle_and_forward(self, conv_info: ConvHolder) -> None:
        handle_dict = self.handle(conv_info)
        if handle_dict:
            if handle_dict["type"] == "system":
                conv_info.to_system_alert(handle_dict["content"])
                await self.a_system_alert(conv_info)
            elif handle_dict["type"] == "new_task":
                conv_info.switch_to_agent(handle_dict["switch_task_id"], handle_dict["content"])
                await handle_dict["receiver"].a_new_task(conv_info)
            else:
                conv_info.switch_to_agent(handle_dict["switch_task_id"], handle_dict["content"])
                await handle_dict["receiver"].a_receive(conv_info)

    def handle(self, conv_info: ConvHolder) \
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

        :param conv_info: pusher task id.
        """
        requester = self._agents[conv_info.requester_name]

        responder_name = conv_info.responder_name
        print(f"responder_name: {responder_name}")
        if responder_name is None and self.default_agent and requester.agent_type and requester.agent_type.HUMAN.value == "HUMAN":
            responder_name = self.default_agent.name
        print(f"responder_name: {responder_name}")
        content = conv_info.content

        self.storage and self.storage.add_message(conv_info.conversation_id, conv_info.message("main"))

        if responder_name:
            if responder_name not in self._agents:
                # Handling the case of incorrect recipient name.
                response_type = "system"
                receiver = requester
                current_task_id = conv_info.task_id
                switch_task_id = conv_info.task_id
                sender_name = "system"
                content = f"@{conv_info.requester_name} {responder_name} not exist, do not @{responder_name} again, Also please do not attempt to converse with me, this is just a system message."
            elif re.search(fr'@\w+ {self.task_tag}', content):
                response_type = "new_task"
                receiver = self._agents[responder_name]
                current_task_id = conv_info.task_id
                switch_task_id = conv_info.snowflake_id_generator.next_id()
                sender_name = conv_info.requester_name

                # Establish a relationship between the push task and the receiver task.
                requester.save_sub_to_main_task_id(switch_task_id, conv_info.task_id)
                receiver.save_main_to_sub_task_id(conv_info.conversation_id, conv_info.task_id, switch_task_id)
            else:
                receiver = self._agents[responder_name]
                sender_name = conv_info.requester_name
                current_task_id = conv_info.task_id
                switch_task_id = conv_info.task_id
                sub_task_id = receiver.convert_main_to_sub_task_id(conv_info.task_id)
                if sub_task_id:
                    # Translate the session ID of the requester into the sub-session ID of the receiver.
                    switch_task_id = sub_task_id
                main_task_id = receiver.convert_sub_to_main_task_id(conv_info.task_id)
                if main_task_id:
                    # Translate the session id of the sender into the superior session id of the receiver.
                    switch_task_id = main_task_id
                if switch_task_id == conv_info.task_id:
                    latest_task_id = receiver.get_conversation_latest_task(conv_info.conversation_id)
                    if requester.agent_type and requester.agent_type.HUMAN.value == "HUMAN" and latest_task_id:
                        response_type = "general"
                        switch_task_id = latest_task_id
                        receiver.save_main_to_sub_task_id(conv_info.conversation_id, conv_info.task_id, switch_task_id)
                    else:
                        # If no subtasks of the task from the requester are found, a prompt is needed to create the task first.
                        response_type = "new_task"
                        switch_task_id = conv_info.snowflake_id_generator.next_id()

                        # Establish a relationship between the push task and the receiver task.
                        requester.save_sub_to_main_task_id(switch_task_id, conv_info.task_id)
                        receiver.save_main_to_sub_task_id(conv_info.conversation_id, conv_info.task_id, switch_task_id)
                        # Create a new task.
                        content = content.replace(f"@{responder_name} ", f"@{responder_name} {self.task_tag} ")
                else:
                    response_type = "general"
        else:
            # Handling the situation where the recipient is not recognized.
            if requester.pipeline != "\\":
                response_type = "system"
                receiver = requester
                current_task_id = conv_info.task_id
                switch_task_id = conv_info.task_id
                sender_name = "system"
                content = f"@{conv_info.requester_name} Any reply must start with @ + recipient's name, Also please do not attempt to converse with me, this is just a system message."
            else:
                return
        if (
                self.default_agent_config.main_model_config.request_config.max_conv_turns >= conv_info.response_proxy.conv_turns) or not conv_info.response_proxy.need_to_stop():
            conv_info.response_proxy.conv_turns += 1
            return {"type": response_type, "receiver": receiver, "receiver_name": receiver.name,
                    "current_task_id": current_task_id, "switch_task_id": switch_task_id,
                    "sender_name": sender_name, "content": content}
        else:
            return

    def system_alert(self, conv_info: ConvHolder) -> None:
        self.storage and self.storage.add_message(conv_info.conversation_id, conv_info.message("system"))
        conv_info.response(0, "system", "", conv_info.content, conv_info.completion_tokens, None)
        conv_info.response(1, "system", "", '[DONE]', 0, None)
        # conv_info.response_proxy.send(conv_info.msg_id, conv_info.task_id, conv_info.requester_name, 0, "system", conv_info.content, conv_info.completion_tokens, None)
        self._agents[conv_info.responder_name].receive(conv_info)

    async def a_system_alert(self, conv_info: ConvHolder) -> None:
        self.storage and self.storage.add_message(conv_info.conversation_id, conv_info.message("system"))
        await conv_info.a_response(0, "system", "", conv_info.content, conv_info.completion_tokens, None)
        await conv_info.a_response(1, "system", "", '[DONE]', 0, None)
        # await conv_info.response_proxy.a_send(conv_info.msg_id, conv_info.task_id, conv_info.requester_name, 0, "system", conv_info.content, conv_info.completion_tokens, None)
        await self._agents[conv_info.responder_name].a_receive(conv_info)
