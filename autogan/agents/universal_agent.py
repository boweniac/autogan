from collections import defaultdict
from typing import Optional, Dict, Any

from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.oai.conv_holder import ConvHolder
from autogan.utils.compressed_messages_utils import compressed_messages
from autogan.utils.compressed_text_utils import compressed_text_universal
from autogan.oai.chat_config_utils import AgentConfig
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.oai.chat_generate_utils import a_generate_chat_completion, generate_chat_completion
from autogan.utils.environment_utils import environment_info
from autogan.protocol.switch_protocol import SwitchProtocol
from enum import Enum

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x


class AgentType(Enum):
    HUMAN = "HUMAN"
    TOOL = "TOOL"
    TOOLMAN = "TOOLMAN"


class UniversalAgent:
    def __init__(
            self,
            name: str,
            duty: str,
            agent_config: Optional[Dict] = None,
            work_flow: Optional[str] = None,
            agent_type: Optional[str] = None,
    ):
        """Agent base class

        Each agent can communicate with other agents in the current department and the leader of the subordinate department to complete tasks together.
        每个 agent 可与当前部门的其他 agent 以及下级部门的 leader 沟通，协作完成任务。

        To provide functions beyond the modeling capabilities for the agent, you can override the tool_function method.
        想要为 agent 提供模型能力之外的功能，可以通过重写 tool_function 方法来实现。

        :param name: The agent name should be unique in the organizational structure.
            agent name 在组织架构中应当是唯一的。
        :param agent_config: The agent configuration includes:
            agent 配置包括：
            - main_model: The LLM configuration of the agent's main body.
                agent 主体的 LLM 配置。
            - summary_model: The LLM configuration used for compressing context and generating text summaries.
                用于压缩上下文以及生成文本摘要的 LLM 配置。
            - request_interval_time: The interval time of LLM requests.
                LLM 请求间隔时间。
            - request_timeout:The timeout of LLM requests.
                LLM 请求超时时间。
            - max_retries: The maximum number of retries for LLM requests.
                LLM 请求最大重试次数。
        :param duty: Used to explain one's job responsibilities to other agents.
            用于向其他 agent 说明自己的工作职责。
        :param work_flow: Defines the workflow of the agent.
            定义 agent 的工作流程。
        :param agent_type: Defines the mode of the agent using the tool_function:
            定义 agent 使用 tool_function 的模式：
            - None: means not using the tool function.
                不使用工具函数。
            - only: Do not use the LLM, only use the tool function to generate results.
                不使用 LLM，仅使用工具函数生成结果。
            - join: The content generated by the LLM will be used as the input parameter for the tool_function.
                LLM 生成的内容将作为 tool_function 的输入参数
        """
        self.name = name
        self.switch: Optional[SwitchProtocol] = None
        self.agent_config = AgentConfig(agent_config) if agent_config else None
        self.duty = duty
        self.workmates = ""  # relevant personnel's name and duty
        self.pipeline = ""  # In a linear workflow, this is the next person to communicate with.
        # Translate the session ID of the pusher into the sub-session ID of the receiver.
        self._sub_to_main_task_id = defaultdict(int)
        # Translate the session id of the sender into the superior session id of the receiver.
        self._main_to_sub_task_id = defaultdict(int)
        self._work_flow = work_flow
        self._agent_type:AgentType = None if agent_type is None else AgentType(agent_type)
        self._conversation_messages = defaultdict(list)  # key: task id，value: Conversation history
        self._conversation_focus = defaultdict(Dict)  # key: task id，value: {"task_publisher": "", "task_content": ""}

    @property
    def get_agent_config(self) -> AgentConfig:
        if self.agent_config:
            return self.agent_config
        else:
            return self.switch.default_agent_config

    def _save_task_info(self, task_id: int, task_info: dict) -> None:
        self.switch.storage and self.switch.storage.save_task_info(task_id, task_info)
        self._conversation_focus[task_id] = task_info

    def _get_task_info(self, task_id: int) -> Optional[dict]:
        if task_id in self._conversation_focus and self._conversation_focus[task_id]:
            return self._conversation_focus[task_id]
        elif self.switch.storage:
            return self.switch.storage.get_task_info(task_id)

    def save_main_to_sub_task_id(self, main_task_id: int, sub_task_id: int) -> None:
        self.switch.storage and self.switch.storage.save_main_to_sub_task_id(main_task_id, sub_task_id)
        self._main_to_sub_task_id[main_task_id] = sub_task_id

    def convert_main_to_sub_task_id(self, task_id: int) -> Optional[int]:
        if task_id in self._main_to_sub_task_id and self._main_to_sub_task_id[task_id]:
            return self._main_to_sub_task_id[task_id]
        elif self.switch.storage:
            return self.switch.storage.convert_main_to_sub_task_id(task_id)

    def save_sub_to_main_task_id(self, sub_task_id: int, main_task_id: int) -> None:
        self.switch.storage and self.switch.storage.save_sub_to_main_task_id(sub_task_id, main_task_id)
        self._sub_to_main_task_id[sub_task_id] = main_task_id

    def convert_sub_to_main_task_id(self, task_id: int) -> Optional[int]:
        if task_id in self._sub_to_main_task_id and self._sub_to_main_task_id[task_id]:
            return self._sub_to_main_task_id[task_id]
        elif self.switch.storage:
            return self.switch.storage.convert_sub_to_main_task_id(task_id)

    def _save_compressed_messages(self, task_id: int, messages: list) -> None:
        self.switch.storage and self.switch.storage.save_compressed_messages(task_id, messages)
        self._conversation_messages[task_id] = messages

    def _add_compressed_message(self, task_id: int, message: dict) -> None:
        self.switch.storage and self.switch.storage.add_compressed_message(task_id, message)
        self._conversation_messages[task_id].append(message)

    def _get_compressed_messages(self, task_id: int) -> Optional[list]:
        if task_id in self._conversation_messages and self._conversation_messages[task_id]:
            return self._conversation_messages[task_id]
        elif self.switch.storage:
            return self.switch.storage.get_compressed_messages(task_id)

    def new_task(self, conv_info: ConvHolder):
        """Accept tasks posted by other agent.

        :param conv_info:
        """
        # Avoid excessively long task content
        if ((self._agent_type != AgentType.TOOL and self._agent_type != AgentType.HUMAN) and conv_info.completion_tokens >
                self.get_agent_config.main_model_config.request_config.max_messages_tokens * 0.5):
            conv_info.to_system_alert(f"@{conv_info.requester_name} The task is too long")
            self.switch.system_alert(conv_info)
        else:
            # Cache task information to maintain focus during task execution
            task_content = conv_info.content.replace(f"@{self.name}", "please help me")
            task_content = task_content.replace(f"{self.switch.task_tag}", "")
            self._save_task_info(conv_info.task_id, {'task_publisher': conv_info.requester_name,
                                                     'task_content': task_content, 'task_publisher_type': conv_info.requester_type})
            # Start the generation process
            self._generate_process(conv_info)

    async def a_new_task(self, conv_info: ConvHolder):
        """Accept tasks posted by other agent.

        :param conv_info: 
        """
        # Avoid excessively long task content
        if ((self._agent_type != AgentType.TOOL and self._agent_type != AgentType.HUMAN) and conv_info.completion_tokens >
                self.get_agent_config.main_model_config.request_config.max_messages_tokens * 0.5):
            conv_info.to_system_alert(f"@{conv_info.requester_name} The task is too long")
            await self.switch.a_system_alert(conv_info)
        else:
            # Cache task information to maintain focus during task execution
            task_content = conv_info.content.replace(f"@{self.name}", "please help me")
            task_content = task_content.replace(f"{self.switch.task_tag}", "")
            self._save_task_info(conv_info.task_id, {'task_publisher': conv_info.requester_name,
                                                     'task_content': task_content, 'task_publisher_type': conv_info.requester_type})
            # Start the generation process
            await self._a_generate_process(conv_info)

    def receive(self, conv_info: ConvHolder):
        """Receive messages sent by other agents (excluding new task requests)

        :param conv_info: 
        """
        if self._agent_type != AgentType.TOOL and self._agent_type != AgentType.HUMAN:
            safe_size = self.get_agent_config.main_model_config.request_config.max_messages_tokens
            if conv_info.completion_tokens > safe_size:
                content, completion_tokens = compressed_text_universal(conv_info.content,
                                                                       self.get_agent_config.summary_model_config,
                                                                       self._get_task_info(conv_info.task_id)[
                                                                           "task_content"],
                                                                       safe_size)
                conv_info.content = content
                conv_info.completion_tokens = completion_tokens
            self._add_compressed_message(conv_info.task_id, {'role': 'user' if conv_info.requester_type == AgentType.HUMAN.value else "assistant",
                                                             'content': conv_info.content,
                                                             'name': conv_info.requester_name,
                                                             'tokens': conv_info.completion_tokens}
                                         )
        self._generate_process(conv_info)

    async def a_receive(self, conv_info: ConvHolder):
        """Receive messages sent by other agents (excluding new task requests)

        :param conv_info: Task id
        """
        if self._agent_type != AgentType.TOOL and self._agent_type != AgentType.HUMAN:
            safe_size = self.get_agent_config.main_model_config.request_config.max_messages_tokens
            if conv_info.completion_tokens > safe_size:
                content, completion_tokens = compressed_text_universal(conv_info.content,
                                                                       self.get_agent_config.summary_model_config,
                                                                       self._get_task_info(conv_info.task_id)[
                                                                           "task_content"],
                                                                       safe_size)
                conv_info.content = content
                conv_info.completion_tokens = completion_tokens
            self._add_compressed_message(conv_info.task_id, {'role': 'user' if conv_info.requester_type == AgentType.HUMAN.value else "assistant",
                                                             'content': conv_info.content,
                                                             'name': conv_info.requester_name,
                                                             'tokens': conv_info.completion_tokens}
                                         )
        await self._a_generate_process(conv_info)

    def _base_message(self, task_id: int) \
            -> tuple[dict[str, str], Optional[dict[str, Any]], int]:
        """This is the paradigm message required for each round of dialogue.
        每轮对话都需要的范式消息

        :param task_id: Task id

        :return:
            -- system_message: Used to clarify its own workflow to the agent and where the agent can seek help.
                用于向 agent 阐明自身工作流程，以及可以向哪些 agent 寻求帮助。
            -- focus_message: Used to maintain focus during task execution, including who is currently executing the task and what the content of the task is. It will not be forgotten or compressed with the increase of dialogue rounds.
                用于在任务执行过程中保持专注力，包括当前正在执行谁发布的任务、任务的内容是什么。不会随会话轮次的增多而被遗忘或压缩。
            -- total_tokens: The overall tokens of the content of the system_message and the focus_message.
                system_message 以及 focus_message 内容的整体 tokens。
        """
        total_tokens = 0

        info = environment_info()

        # Assemble system message
        system_prompt = f"""Now your name is {self.name}, you are an assistant who will not give up easily when you encounter difficulties

Environment information:
{info}"""

        if self._work_flow:
            system_prompt += f"""

Your work flow is::
{self._work_flow}"""

        if self.workmates:
            system_prompt += f"""

The following professionals can help you accomplish the task:
{self.workmates}"""

        if self._agent_type is None:
            system_prompt += f"""
    
    Please follow these guidelines when replying to any content:
    1. Be aware that if you do not @recipient at the beginning, the system will give an error.
    2. When asking for help, you need to first post a task, the method is: @recipient {self.switch.task_tag} task content.
    3. The recipient does not have any dialogue records before the task begins, nor can they see your conversations with others.
    4. Do not suggest the recipient to communicate with others.
    5. Do not explain to the initiator of the task what you are going to do.
    6. In the reply, do not converse with two recipients at the same time.
            """

        total_tokens += 37

        system_message = {'role': 'system', 'content': system_prompt}

        conversation_focus = self._get_task_info(task_id)
        if conversation_focus:
            # Assemble focus message
            focus_prompt = f"""current task content:
task issuer: {conversation_focus['task_publisher']}
task content: {conversation_focus['task_content']}"""

            if self._agent_type is None:
                if self.pipeline and self.pipeline != "\\":
                    focus_prompt += f"""

When you have the result of the task, please @{self.pipeline} {self.switch.task_tag} and reply to the execution result, He'll know what to do next"""
                else:
                    focus_prompt += f"""

When you have the result of the task, please @{conversation_focus['task_publisher']} and reply to the execution result"""

            total_tokens += count_text_tokens(focus_prompt)

            focus_message = {'role': 'user' if conversation_focus['task_publisher_type'] == AgentType.HUMAN.value else "assistant", 'content': focus_prompt, 'name': conversation_focus['task_publisher']}
        else:
            focus_message = None

        return system_message, focus_message, total_tokens

    def _consider_message(self, ideas: dict, index: int, task_publisher: str) \
            -> tuple[tuple[str, dict], bool]:
        """Thought prompts, with new content requested at each level
        深思提示词，每层请求新的内容

        :param task_id: Task id
        :param ideas: Results generated
        :param index: Current thinking depth

        :return:
            -- message_list: Thought prompts list
                -- tag:
                -- message: Thought prompts
            -- is_end:
        """
        messages = []

        task_submission = ""
        if self.pipeline and self.pipeline != "\\":
            task_submission += f"{self.pipeline} : When there is no more work to be done, Submit the results to me."
        else:
            task_submission += f"{task_publisher} : When there is no more work to be done, Submit the results to me."

        info = f"""

reference workflow:
{environment_info()}"""

        workmates = ""
        if self.workmates:
            workmates = f"""

relevant personnel's name and duty:
{self.workmates}
{task_submission}"""

        workflow = ""
        if self._work_flow:
            workflow = f"""
{self._work_flow}"""

        repetitive_prompt = f"""The above is a group chat record,  assuming you are {self.name}, please do the following analysis:

Step 1: Understand your overall workflow (No need to output):
    workflow:{workflow}

Step 2: Analyze whether {self.name} is repeating a task in the workflow or encountering difficulties (No need to output).

Step 3: output your analysis results
    If yes, please give advice on how to stop repeating from the perspective of {self.name}.
    If not, please reply one word 'None'."""

        messages.append(("Observe whether the previous conversation fell into a cycle",
                         {'role': 'system', 'content': repetitive_prompt}))

        debug_prompt = f"""The above is a group chat record, please do the following analysis:

Step 1: Understand your overall workflow, Including the execution conditions and objectives for each step (No need to output):
    workflow:{workflow}
    
Step 2: Analyze whether there are unresolved errors in the previous conversation (No need to output).

Step 3: Analyze If there are unresolved errors, Think about what the root cause of these errors is (No need to output).

Step 4: Analyze If there are unresolved errors, From {self.name}'s perspective, how should you solve it next?  (No need to output)

Step 5: output your analysis results, including the following content:
    whether there are unresolved errors in the previous conversation:
        If there are unresolved errors, What errors in the dialogue:
        If there are unresolved errors, The root cause of the error:
        If there are unresolved errors, How to solve it next:

Note: There's no need to output the specific dialogue content, just output the analysis results."""

        messages.append(("Reflect on whether there are any errors in the previous dialogue process",
                         {'role': 'system', 'content': debug_prompt}))

        planning_prompt = f"""The above is a group chat record, assuming you are {self.name}, please do the following analysis:

Step 1: Understand your overall workflow (No need to output):
    workflow:{workflow}

Step 2: Analyze which item to execute or continue to execute in the workflow (No need to output).

Step 3: Understand the specific errors that have occurred in the current conversation (No need to output).
    Are you stuck in a deadlock: {ideas["Observe whether the previous conversation fell into a cycle"]}
    
    {ideas["Reflect on whether there are any errors in the previous dialogue process"]}

Step 4: Understand some rules (No need to output).
    1. When asking for help, you need to first post a task,
    2. The recipient does not have any dialogue records before the task begins, nor can they see your conversations with others.
    2. Don't let the other party to communicate with others.
    3. In your plan, there should be no content about apologizing to others or what you are going to do.

Step 5: output your analysis results, including the following content:
    Do you need to create a task:
    In the next round of conversation, the specific work you need to do is(Please explain in detail and Ignore the work that has been completed.):
    all the details that need to be taken into consideration, including recommended methods or tools, etc:

Note: There's no need to output the specific dialogue content, just output the analysis results.
"""

        messages.append(("Think about what to do next", {'role': 'system', 'content': planning_prompt}))

        communicate_prompt = f"""your name is {self.name}, please do the following analysis:
        
Step 1: Understand your work plan (No need to output):
    {ideas["Think about what to do next"]}

Step 2: Get to know your colleagues, including what they can and cannot do (No need to output):
    {workmates}
    {task_publisher} : ""
    
Step 3: Analyze who is the most relevant colleague to the first step of next round of conversation the specific work you need to do, note that you can only choose one person (No need to output).

Step 4: output your analysis results, including the following content:
    who is the most relevant colleague to the first step of your plan:
    What are the requirements when the other party receives messages:
    What can the other party do:
    What the other party cannot do:
    
Note: please provide the correct names of relevant personnel, Don't provide names that don't exist."""

        messages.append(("Think about who to communicate with next", {'role': 'user', 'content': communicate_prompt}))

        reply_prompt = f"""The above is a group chat record, assuming you are {self.name}, Please strictly follow the contents of the guidelines below to generate your response, note do not communicate with others or perform other tasks:

{info}

Step 1: Clarify who you will be communicating with (No need to output):
    {ideas["Think about who to communicate with next"]}

Step 2: Specify the task you are going to carry out (No need to output):
    {ideas["Think about what to do next"]}

Step 3: Understand some response rules (No need to output).
    1. Please do not mention the second person in your reply content.
    2. When you need to post a task, the method is: @recipient {self.switch.task_tag} task content.

Step 4: Please follow the content of the previous step, From {self.name}'s perspective, Output your response in the format below:
    @who you will be communicating with + Reply content"""

        messages.append(("Generate reply content", {'role': 'system', 'content': reply_prompt}))

        if index == len(messages) - 1:
            return messages[index], True
        else:
            return messages[index], False

    def _chat_messages_safe_size(self, task_id: int, safe_size: int) \
            -> tuple[list, int]:
        """Compress the historical session records within the current task scope (excluding system_message and focus_message)

        :param task_id: Task id
        :param safe_size: The max_messages_tokens of the main LLM configuration

        :return: --request_messages: It is used for the message content requested to LLM, with the tokens field of each message removed.
            –-total_tokens: The overall tokens after compression.
        """
        comp_messages = self._get_compressed_messages(task_id)
        if comp_messages:
            conversation_messages, request_messages, total_tokens = compressed_messages(
                comp_messages, self._get_task_info(task_id)["task_content"],
                self.get_agent_config.summary_model_config, safe_size)

            if request_messages:
                self._save_compressed_messages(task_id, conversation_messages)
                return request_messages, total_tokens

        return [], 0

    def _base_generate_reply(self, task_id: int) -> list:
        """Use the main LLM to generate responses.

        Before generating a response, the historical conversation records within the current task scope, excluding system_message and focus_message, will be compressed first.

        :param task_id: Task id

        :return: --content: Generate content
            --tokens: Generate content tokens
        """
        system_message, focus_message, total_tokens = self._base_message(task_id)

        # Calculate the target size of context compression.
        safe_size = self.get_agent_config.main_model_config.request_config.max_messages_tokens - total_tokens
        # Compress the historical conversation records.
        request_messages, total_tokens = self._chat_messages_safe_size(task_id, safe_size)
        request_messages.insert(0, system_message)
        if focus_message:
            request_messages.insert(0, focus_message)
        return request_messages

    def _consider_generate(self, ideas: Dict, task_id: int, request_messages: list) -> tuple[list, str]:
        """Use the main LLM to generate responses.

        Before generating a response, the historical conversation records within the current task scope, excluding system_message and focus_message, will be compressed first.

        :param task_id: Task id

        :return: --content: Generate content
            --tokens: Generate content tokens
        """
        index = 0
        while True:
            message, is_end = self._consider_message(ideas, index, self._get_task_info(task_id)["task_publisher"])
            if is_end:
                gen = "main"
            else:
                gen = "idea"

            print(
                colored(
                    f"\n\n>>>>>>>> {message[0]}:",
                    "cyan",
                ),
                flush=True,
            )

            if message[1]["role"] == "system":
                messages = request_messages.copy()
                messages.append(message[1])
            else:
                messages = [message[1]]

            yield messages, message[0], gen
            if is_end:
                break
            index += 1

    def tool_function(self, task_id: int, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        """When the value of the tool_function_usage parameter is 'only' or 'join', please override this method.

        :return: --content: Generate content
            --tokens: Generate content tokens
        """
        pass

    def use_tool(self, task_id: int, content: str, completion_tokens: int, sender_name: str) -> tuple[str, int]:
        """When the value of the tool_function_usage parameter is 'only' or 'join', please override this method.

        :return: --content: Generate content
            --tokens: Generate content tokens
        """
        content, completion_tokens = self.tool_function(task_id, content, completion_tokens)
        # 设置接收者
        if not content.startswith("@"):
            if self.pipeline and self.pipeline != "\\":
                receiver = self.pipeline
            else:
                receiver = self._get_task_info(task_id)["task_publisher"]
                if not receiver:
                    receiver = sender_name
            content = f"@{receiver} " + content
        return content, completion_tokens

    def _generate_process(self, conv_info: ConvHolder):
        """Generate process

        If the value of the tool_function_usage parameter is None, only the main LLM is used to generate a response.
        如果 tool_function_usage 参数的值为 None，则仅使用主体 LLM 生成回复。

        If the value of the tool_function_usage parameter is 'only', the main LLM is skipped and the tool_function is used directly to generate a response.
        如果 tool_function_usage 参数的值为 only，则跳过主体 LLM 直接使用 tool_function 生成回复。

        If the value of the tool_function_usage parameter is 'join', the main LLM is first used to generate content, and then the generated content is used as the input parameter for tool_function.
        如果 tool_function_usage 参数的值为 join，则先使用主体 LLM 生成内容，然后将生成的内容作为 tool_function 的输入参数。
        """
        requester = conv_info.requester_name
        content = ""
        completion_tokens = 0
        try:
            conv_info.init_message(self.name, None if self._agent_type is None else self._agent_type.value)
            # 生成回复内容
            if self._agent_type != AgentType.TOOL and self._agent_type != AgentType.HUMAN:
                request_messages = self._base_generate_reply(conv_info.task_id)
                if self.switch.default_consider_mode == "on" or ((
                                                                         self.switch.default_consider_mode == "auto" or self.switch.default_consider_mode is None) and "gpt-4" not in self.get_agent_config.main_model_config.model):
                    ideas = defaultdict(str)
                    for messages, idea_tag, gen in self._consider_generate(ideas, conv_info.task_id, request_messages):
                        request_data = ChatCompletionsRequest(messages, self.switch.default_stream_mode)
                        content, completion_tokens = generate_chat_completion(
                            self.get_agent_config.main_model_config, request_data, conv_info, gen)
                        ideas[idea_tag] = content
                else:
                    request_data = ChatCompletionsRequest(request_messages, self.switch.default_stream_mode)
                    content, completion_tokens = generate_chat_completion(
                        self.get_agent_config.main_model_config, request_data, conv_info, "main")

                if not content:
                    raise ValueError("Failed to generate content.")

            if content:
                # 防止模型 @ 自己
                content = content.replace(f"@{self.name} ", "")

            # 使用工具
            if (self._agent_type == AgentType.TOOL and self._agent_type == AgentType.HUMAN) or (
                    self._agent_type == AgentType.TOOLMAN and not content.startswith("@")):
                content, completion_tokens = self.use_tool(conv_info.task_id, content, completion_tokens, requester)
                conv_info.response(0, "tool", content, completion_tokens, None)
                # conv_info.response_proxy.send(conv_info.msg_id, conv_info.task_id, conv_info.requester_name, 0, "tool", content, completion_tokens, None)
            self._add_compressed_message(conv_info.task_id,
                                         {'role': 'user' if self._agent_type == AgentType.HUMAN else 'assistant', 'name': self.name, 'content': content, 'tokens': completion_tokens})
            conv_info.update_message(content)
            self.switch.handle_and_forward(conv_info)
        except SystemExit:
            print("The task is finished.")
        except Exception as e:
            print(f"generate_process :{e}")
            if (self._agent_type == AgentType.TOOL and self._agent_type == AgentType.HUMAN):
                conv_info.to_system_alert(f"@{requester} Generate error, Please trying again")
                self.switch.system_alert(conv_info)

    async def _a_generate_process(self, conv_info: ConvHolder):
        """Generate process

        If the value of the tool_function_usage parameter is None, only the main LLM is used to generate a response.
        如果 tool_function_usage 参数的值为 None，则仅使用主体 LLM 生成回复。

        If the value of the tool_function_usage parameter is 'only', the main LLM is skipped and the tool_function is used directly to generate a response.
        如果 tool_function_usage 参数的值为 only，则跳过主体 LLM 直接使用 tool_function 生成回复。

        If the value of the tool_function_usage parameter is 'join', the main LLM is first used to generate content, and then the generated content is used as the input parameter for tool_function.
        如果 tool_function_usage 参数的值为 join，则先使用主体 LLM 生成内容，然后将生成的内容作为 tool_function 的输入参数。
        """
        requester = conv_info.requester_name
        content = ""
        completion_tokens = 0
        try:
            conv_info.init_message(self.name, None if self._agent_type is None else self._agent_type.value)
            # 生成回复内容
            if (self._agent_type != AgentType.TOOL and self._agent_type != AgentType.HUMAN):
                request_messages = self._base_generate_reply(conv_info.task_id)
                if self.switch.default_consider_mode == "on" or ((
                                                                         self.switch.default_consider_mode == "auto" or self.switch.default_consider_mode is None) and "gpt-4" not in self.get_agent_config.main_model_config.model):
                    ideas = defaultdict(str)
                    for messages, idea_tag, gen in self._consider_generate(ideas, conv_info.task_id, request_messages):
                        request_data = ChatCompletionsRequest(messages, self.switch.default_stream_mode)
                        content, completion_tokens = await a_generate_chat_completion(
                            self.get_agent_config.main_model_config, request_data, conv_info, gen)
                        ideas[idea_tag] = content
                else:
                    request_data = ChatCompletionsRequest(request_messages, self.switch.default_stream_mode)
                    content, completion_tokens = await a_generate_chat_completion(
                        self.get_agent_config.main_model_config, request_data, conv_info, "main")

                if not content:
                    # 防止模型 @ 自己
                    raise ValueError("Failed to generate content.")

            # 使用工具
            if (self._agent_type == AgentType.TOOL and self._agent_type == AgentType.HUMAN) or (
                    self._agent_type == AgentType.TOOLMAN and not content.startswith("@")):
                content, completion_tokens = self.use_tool(conv_info.task_id, content, completion_tokens, requester)
                await conv_info.a_response(0, "tool", content, completion_tokens, None)
                # await conv_info.response_proxy.a_send(conv_info.msg_id, conv_info.task_id, conv_info.requester_name, 0, "tool", content, completion_tokens, None)
            self._add_compressed_message(conv_info.task_id,
                                         {'role': 'user' if self._agent_type == AgentType.HUMAN else 'assistant', 'name': self.name, 'content': content, 'tokens': completion_tokens})
            conv_info.update_message(content)
            await self.switch.a_handle_and_forward(conv_info)
        except SystemExit:
            print("The task is finished.")
        except Exception as e:
            print(f"generate_process :{e}")
            if (self._agent_type == AgentType.TOOL and self._agent_type == AgentType.HUMAN):
                conv_info.to_system_alert(f"@{requester} Generate error, Please trying again")
                await self.switch.a_system_alert(conv_info)
