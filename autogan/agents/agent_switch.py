import re
import uuid
import time
from typing import List, Optional, Dict
from autogan.utils.response import default_response_func, ResponseFuncType


class AgentSwitch:
    def __init__(
            self,
            organizational_structure: List,
            task_tag: Optional[str] = "/task",
            opening_speaker: Optional[any] = None,
            default_agent_config: Optional[Dict] = None,
            default_super_rich: Optional[str] = None,
            default_stream_mode: Optional[bool] = None,
            response_func: Optional[ResponseFuncType]
            = default_response_func,
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

        :param organizational_structure: A multidimensional list containing agent objects.
            一个包含 agent 对象的多维列表。
        :param opening_speaker_name: The name of the human agent invited to publish the first task.
            被邀请发布第一个任务的人工 agent 名称。
        :param task_tag: Publish tasks to other agents by adding task_tag to the message.
            通过在消息中添加 task_tag 来向其他 agent 发布任务。
        """
        self.task_tag = task_tag
        self._default_agent_config = default_agent_config
        self._default_super_rich = default_super_rich
        self._default_stream_mode = default_stream_mode
        self._response_func = response_func
        self._agents = {}  # key: agent name value: agent object

        self._init_agents(organizational_structure)
        self._init_agents_workmates(organizational_structure)
        if opening_speaker:
            self._inviting_to_speak(opening_speaker)

    def _init_agents(self, agent_list: list):
        for item in agent_list:
            if isinstance(item, list):
                self._init_agents(item)
            elif isinstance(item, str):
                continue
            else:
                self._agents[item.name] = item
                if item.agent_config is None and self._default_agent_config is not None:
                    item.set_agent_config(self._default_agent_config)
                if item.super_rich is None and self._default_super_rich is not None:
                    item.super_rich = self._default_super_rich
                if item.stream_mode is None:
                    if self._default_stream_mode is None or self._default_stream_mode:
                        item.stream_mode = True
                    else:
                        item.stream_mode = False
                if self._response_func:
                    item.response_func = self._response_func

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
            l = len(agent_list)

            for index, main_agent in enumerate(agent_list):
                # Skip the first element
                if index == 0:
                    continue

                workmates = ""

                if index == l - 1:
                    # If this is the last element
                    name = "\\"
                elif isinstance(agent_list[index + 1], list):
                    # If the next element is a list
                    name = agent_list[index + 1][0].name
                    duty = agent_list[index + 1][0].duty
                    workmates = f"""
{name} : {duty}"""
                else:
                    # If the next element is agent
                    name = agent_list[index + 1].name
                    duty = agent_list[index + 1].duty
                    workmates = f"""
{name} : {duty}"""

                if isinstance(main_agent, list):
                    # If the current element is a list
                    self._init_agents_workmates(main_agent)
                    if not main_agent[0].pipeline or main_agent[0].pipeline == "\\":
                        main_agent[0].workmates += workmates
                        main_agent[0].pipeline = name
                else:
                    # If the current element is agent
                    if not main_agent.pipeline or main_agent.pipeline == "\\":
                        main_agent.workmates += workmates
                        main_agent.pipeline = name
        else:
            # The current list is non-workflow mode.
            for main_agent in agent_list:
                workmates = ""

                if isinstance(main_agent, list):
                    # If the current element is a list
                    self._init_agents_workmates(main_agent)

                    # If the current element is a workflow list, no hierarchical relationship is established.
                    if isinstance(main_agent[0], str):
                        continue

                    # Establish a leveling relationship between current department leaders
                    for agent in agent_list:
                        if isinstance(agent, list):
                            # If other elements are lists

                            if isinstance(agent[0], str):
                                if agent[0] == "F":
                                    # If it is a workflow

                                    # Determine whether the second element is a list.
                                    if isinstance(agent[1], list):
                                        name = agent[1][0].name
                                        duty = agent[1][0].duty
                                    else:
                                        name = agent[1].name
                                        duty = agent[1].duty
                                else:
                                    # Skip other types of workflow
                                    continue
                            else:
                                # If it is a department
                                if agent[0].name != main_agent[0].name and agent[0].duty is not None:
                                    name = agent[0].name
                                    duty = agent[0].duty
                                else:
                                    # Skip departments that duplicate the current department
                                    continue
                        else:
                            # If other elements are agent
                            name = agent.name
                            duty = agent.duty
                        workmates += f"""
{name} : {duty}"""
                    main_agent[0].workmates += workmates
                else:
                    # If the current element is agent

                    # Establish a level relationship of the current agent
                    for agent in agent_list:
                        if isinstance(agent, list):
                            # If other elements are lists

                            # Determine whether it is a department or a workflow
                            if isinstance(agent[0], str):
                                if agent[0] == "F":
                                    # If it is a workflow

                                    # Determine whether the second element is a list.
                                    if isinstance(agent[1], list):
                                        name = agent[1][0].name
                                        duty = agent[1][0].duty
                                    else:
                                        name = agent[1].name
                                        duty = agent[1].duty
                                else:
                                    # Skip other types of workflow
                                    continue
                            else:
                                # If it is a department
                                name = agent[0].name
                                duty = agent[0].duty
                        else:
                            # If other elements are agent
                            if agent.name != main_agent.name and agent.duty is not None:
                                name = agent.name
                                duty = agent.duty
                            else:
                                # Skip the duplicate agent with the current agent
                                continue
                        workmates += f"""
{name} : {duty}"""
                    main_agent.workmates += workmates

    def _inviting_to_speak(self, invited_speaker):
        """Invite the human agent to publish the first task
        邀请人工 agent 发布第一个任务

        :param invited_speaker_name: The name of the human agent
            人工 agent 名称。
        """
        if invited_speaker.name not in self._agents:
            print("agent does not exist")
            return
        new_task_id = self.create_time_based_uuid()
        invited_speaker.receive(self, new_task_id, "system", "Please enter", 2)

    def handle_and_forward(self, task_id: str, pusher_name: str, content: str,
                           completion_tokens: Optional[int]):
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

        if match:
            if match[0] not in self._agents:
                # Handling the case of incorrect recipient name.
                warn = f"@{pusher_name} {match[0]} not exist, do not @{match[0]} again, Also please do not attempt to converse with me, this is just a system message."
                self._response_func("system", "system", "", False, 0, warn, 0, None)
                pusher.receive(self, task_id, "system", warn, 12)

            # Get receiver object.
            receiver = self._agents[match[0]]
            if re.search(fr'@\w+ {self.task_tag}', content):
                # Generate a new task id.
                new_task_id = self.create_time_based_uuid()

                # Establish a relationship between the push task and the receiver task.
                pusher.sub_to_main_task_id[new_task_id] = task_id
                receiver.main_to_sub_task_id[task_id] = new_task_id
                # Create a new task.
                receiver.new_task(self, new_task_id, pusher_name, content, completion_tokens)
            else:
                switch_task_id = task_id
                if receiver.main_to_sub_task_id and task_id in receiver.main_to_sub_task_id:
                    # Translate the session ID of the pusher into the sub-session ID of the receiver.
                    switch_task_id = receiver.main_to_sub_task_id[task_id]
                if receiver.main_to_sub_task_id and task_id in receiver.sub_to_main_task_id:
                    # Translate the session id of the sender into the superior session id of the receiver.
                    switch_task_id = receiver.sub_to_main_task_id[task_id]
                if switch_task_id == task_id:
                    # If no subtasks of the task from the pusher are found, a prompt is needed to create the task first.
                    # Generate a new task id.
                    new_task_id = self.create_time_based_uuid()

                    # Establish a relationship between the push task and the receiver task.
                    pusher.sub_to_main_task_id[new_task_id] = task_id
                    receiver.main_to_sub_task_id[task_id] = new_task_id
                    # Create a new task.
                    content = content.replace(f"@{match[0]} ", f"@{match[0]} {self.task_tag} ")
                    receiver.new_task(self, new_task_id, pusher_name, content, completion_tokens)
                else:
                    receiver.receive(self, switch_task_id, pusher_name, content, completion_tokens)
        else:
            # Handling the situation where the recipient is not recognized.
            if pusher.pipeline != "\\":
                warn = f"@{pusher_name} Any reply must start with @ + recipient's name, Also please do not attempt to converse with me, this is just a system message."
                self._response_func("system", "system", "", False, 0, warn, 0, None)
                pusher.receive(self, task_id, "system", warn, 12)

    @staticmethod
    def create_time_based_uuid():
        # 获取当前时间的时间戳
        timestamp = time.time()

        # 创建一个基于时间戳的UUID
        return uuid.uuid5(uuid.NAMESPACE_DNS, str(timestamp))
