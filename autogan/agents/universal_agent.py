from collections import defaultdict
from typing import Optional, Dict, Any, Union, Tuple, List
from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.oai.conv_holder import DialogueManager
from autogan.prompt.agent.consider_prompts import ConsiderPrompts
from autogan.prompt.agent.universal_agent_prompts import UniversalAgentPrompt
from autogan.utils.compressed_messages_utils import compressed_messages
from autogan.oai.chat_config_utils import AgentLLMConfig
from autogan.oai.chat_generate_utils import a_generate_chat_completion, generate_chat_completion
from autogan.protocol.switch_protocol import SwitchProtocol

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x


class UniversalAgent:
    def __init__(
            self,
            name: str,
            duty: str | dict,
            work_flow: Optional[str] | Optional[dict] = None,
            agent_type: Optional[str] = None,
            agent_llm_config: Optional[Dict] = None,
    ):
        """通用 agent 类，所有自定义 agent 应继承该类。
        
        agent 有四种类型，分别是：AGENT，HUMAN，TOOLMAN，TOOL。可在初始化 agent 时，通过 agent_type 参数定义。
            - AGENT：（默认）普通 agent，通过 LLM 驱动。如其回复的内容没有 @ 任何人，将触发系统纠错机制，被要求重新生成回复。
            - HUMAN：人类的数字化身，人类可通过 HUMAN 类型的 agent 与其他 agent 进行交流。
            - TOOLMAN：该类型的 agent，如其回复的内容没有 @ 任何人，将被视为工具函数调用请求。
            - TOOL：禁用 LLM，该类型 agent 所接收到的消息，将直接作为参数传递给工具函数。

        自定义工具函数，需重写 tool_parameter_identification 和 tool_function 方法。
            - tool_parameter_identification：（非必须，默认透传消息内容）用来从回复内容中识别出，需要调用的函数类型和调用参数。
            - tool_function：根据 tool_parameter_identification 的识别结果，实现工具调用。

        :param name: agent 名称，必须使用英文，不能出现空格，且在组织架构中唯一。
        :param duty: 用于向其他 agent 说明自己的工作职责。支持字符串和字典（多语言），当值为字典时 "EN" 键为必须。
            duty 的内容建议包含：
                - 自己能做什么
                - 自己不能做什么
                - 接收消息的特殊格式（如需）
        :param work_flow: 定义 agent 的工作流程。该内容将被嵌入 agent 的 system 提示词中。
            支持字符串和字典（多语言），当值为字典时 "EN" 键为必须。
        :param agent_type: 定义 agent 的类型，包括 AGENT，HUMAN，TOOLMAN，TOOL。详细描述见上方介绍。
        :param agent_llm_config: agent LLM 配置，此处如未定义，则会使用 switch 的默认配置。：
            - main_model: agent 主体的 LLM 配置。
            - summary_model: 用于压缩上下文以及生成文本摘要的 LLM 配置。
            - request_interval_time: LLM 请求间隔时间。
            - request_timeout: LLM 请求超时时间。
            - max_retries: LLM 请求最大重试次数。
        """
        self.name: str = name
        self._duty: str | dict = duty
        self._work_flow: Optional[str] | Optional[dict] = work_flow
        self.agent_type: str = "AGENT" if agent_type is None else agent_type
        self._agent_llm_config: Optional[AgentLLMConfig] = AgentLLMConfig(agent_llm_config) if agent_llm_config else None

        self.switch: Optional[SwitchProtocol] = None
        self.workmates: str = ""  # 可交流的 agent 以及他们各自的 duty
        self.pipeline: str = ""  # 在流水线模式的下游 agent 及其 duty
        self._sub_to_main_task_id = defaultdict(int)  # 用于通过当前 agent 发布的子任务 id，找到对应的主任务 id
        self._main_to_sub_task_id = defaultdict(int)  # 用于通过主任务 id，找到当前 agent 接受的子任务 id
        self._task_messages = defaultdict(list)  # 存储任务域内的对话记录
        self._task_info = defaultdict(Dict)  # 存储任务信息，用于使 agent 保持专注，不忘记对话目的
        self._conversation_latest_task = defaultdict(int)  # 用于存储当前 agent 在回话内收到的最后一个任务的 id，用于在任务被打断后可以衔接
        self._prompts: Optional[UniversalAgentPrompt] = None  # agent 的动态提示词，根据环境信息和任务内容实时构建提示词

    @property
    def get_duty(self) -> str | dict:
        """获取 agent 工作职责"""
        if isinstance(self._duty, dict):
            return self._duty.get(self.switch.default_language, self._duty["EN"])
        else:
            return self._duty

    @property
    def _get_work_flow(self) -> Optional[str] | Optional[dict]:
        """获取 agent 工作流程"""
        if isinstance(self._work_flow, dict):
            return self._work_flow.get(self.switch.default_language, self._work_flow["EN"])
        else:
            return self._work_flow

    @property
    def get_agent_llm_config(self) -> AgentLLMConfig:
        """获取 agent LLM 配置"""
        if self._agent_llm_config:
            return self._agent_llm_config
        else:
            return self.switch.default_agent_config

    def assign_workmates(self, workmates: str, pipeline: str):
        """为当前 agent 分配同事，并初始化提示词"""
        self.workmates += workmates
        self.pipeline = pipeline
        self._prompts = UniversalAgentPrompt(self.switch.default_language, self.switch.task_tag, self.name, self._get_work_flow, workmates, pipeline)

    def _storage_add_task(self, conv_info: DialogueManager):
        """存储任务信息"""
        if self.switch.storage:
            self.switch.storage.add_task(conv_info.conversation_id, conv_info.pre_task_id, conv_info.sender_name,
                                         conv_info.sender_type, conv_info.task_id,
                                         self.name, self.agent_type, conv_info.content)
        self._task_info[conv_info.task_id] = {'par_agent_name': conv_info.sender_name,
                                              'content': conv_info.content,
                                              'par_agent_type': conv_info.sender_type}

    def _storage_get_task_info(self, task_id: int) -> Optional[dict]:
        """获取任务信息"""
        if task_id in self._task_info and self._task_info[task_id]:
            return self._task_info[task_id]
        elif self.switch.storage:
            task_info = self.switch.storage.get_task_info(task_id)
            self._task_info[task_id] = task_info
            return task_info

    def storage_convert_main_or_sub_task_id(self, task_id: int) -> tuple[Optional[int], Optional[int]]:
        """转换任务 id：将下级任务 id 转换为上级任务 id，或是将上级任务 id 转换为下级任务 id"""
        main_task_id = None
        sub_task_id = None
        if task_id in self._sub_to_main_task_id and self._sub_to_main_task_id[task_id]:
            main_task_id = self._sub_to_main_task_id[task_id]
        if task_id in self._main_to_sub_task_id and self._main_to_sub_task_id[task_id]:
            sub_task_id = self._main_to_sub_task_id[task_id]

        if main_task_id is None and sub_task_id is None:
            main_task_id, sub_task_id = self.switch.storage.convert_main_or_sub_task_id(task_id, self.name)
        return main_task_id, sub_task_id

    def _storage_save_compressed_messages(self, task_id: int, messages: list) -> None:
        """缓存压缩后的任务消息记录"""
        if self.switch.storage:
            self.switch.storage.save_compressed_messages(task_id, messages)
        else:
            self._task_messages[task_id] = messages

    def storage_add_compressed_message(self, conv_info: DialogueManager) -> None:
        """添加任务消息记录"""
        if self.switch.storage:
            self.switch.storage.add_compressed_message(conv_info.task_id, conv_info.compressed_message)
        else:
            self._task_messages[conv_info.task_id].append(conv_info.compressed_message)

    def _storage_get_compressed_messages(self, task_id: int) -> Optional[list]:
        """获取任务消息记录"""
        if task_id in self._task_messages and self._task_messages[task_id]:
            return self._task_messages[task_id]
        elif self.switch.storage:
            return self.switch.storage.get_compressed_messages(task_id)

    def storage_get_conversation_latest_task(self, conversation_id: int) -> int:
        """获取会话中 agent 执行的最后一个任务 id"""
        if conversation_id in self._conversation_latest_task and self._conversation_latest_task[conversation_id]:
            return self._conversation_latest_task[conversation_id]
        elif self.switch.storage:
            return self.switch.storage.get_conversation_latest_task(conversation_id, self.name)

    def new_task(self, conv_info: DialogueManager):
        """接受其他座席交办的任务"""
        if conv_info.sender_type == "HUMAN":
            self.storage_add_compressed_message(conv_info)
        self._storage_add_task(conv_info)
        self._generate_process(conv_info)

    async def a_new_task(self, conv_info: DialogueManager):
        """接受其他座席交办的任务"""
        if conv_info.sender_type == "HUMAN":
            self.storage_add_compressed_message(conv_info)
        self._storage_add_task(conv_info)
        await self._a_generate_process(conv_info)

    def receive(self, conv_info: DialogueManager):
        """接收消息"""
        if self.agent_type != "TOOL" and self.agent_type != "HUMAN":
            self.storage_add_compressed_message(conv_info)
        self._generate_process(conv_info)

    async def a_receive(self, conv_info: DialogueManager):
        """接收消息"""
        if self.agent_type != "TOOL" and self.agent_type != "HUMAN":
            self.storage_add_compressed_message(conv_info)
        await self._a_generate_process(conv_info)

    def _task_info_message(self, task_id: int) -> tuple[Optional[dict[str, Any]], int]:
        """将任务信息封装成消息"""
        task_info = self._storage_get_task_info(task_id)
        if task_info:
            focus_prompt, tokens = self._prompts.build_focus_prompt(task_id, task_info['par_agent_name'],
                                                                    task_info['content'])
            task_message = {
                'role': 'user' if task_info['par_agent_type'] == "HUMAN" else "assistant",
                'content': focus_prompt, 'name': task_info['par_agent_name']}
        else:
            task_message = None
            tokens = 0

        return task_message, tokens

    def _chat_messages_safe_size(self, task_id: int, safe_size: int) \
            -> tuple[list, int]:
        """压缩当前任务范围内的历史会话记录 (不包括system_message和focus_message)

        :param task_id: Task id
        :param safe_size: The max_messages_tokens of the main LLM configuration

        :return: --request_messages: 压缩并去除 tokens 字段的消息记录，用于传入 LLM
            –-total_tokens: 压缩后的总体 tokens
        """
        comp_messages = self._storage_get_compressed_messages(task_id)
        if comp_messages:
            conversation_messages, request_messages, total_tokens = compressed_messages(
                comp_messages, self._storage_get_task_info(task_id)["content"],
                self.get_agent_llm_config.summary_model_config, safe_size)

            if conversation_messages and request_messages:
                self._storage_save_compressed_messages(task_id, conversation_messages)
                return request_messages, total_tokens

        return [], 0

    def tool_parameter_identification(self, content: Optional[str] = None) -> tuple[List[tuple], str, str]:
        """（非必须，默认透传消息内容）用来从回复内容中识别出，需要调用的函数类型和调用参数。

        :return: –-param_list: 待调用的工具和参数列表
                --tool: 待调用的工具
                –-param: 调用工具时的传参
            --start_tag: 开始调用工具时的前端显示标签
            --end_tag: 工具调用结束后的前端显示标签"""
        return [("", content)], "", ""

    def tool_call_function(self, conversation_id: int, task_id: int, tool: str, param: str | dict) -> tuple[str, int]:
        """根据 tool_parameter_identification 识别结果，调用相应工具函数

        :return: --conversation_id: 会话 id
            --task_id: 任务 id
            –-param_list: 待调用的工具和参数列表
                --tool: 待调用的工具
                –-param: 调用工具时的传参
        """
        pass

    def tool_reply(self, conversation_id: int, task_id: int, sender_name: str, param_list: list) -> tuple[str, int]:
        """When the value of the tool_function_usage parameter is 'only' or 'join', please override this method."""
        final_content = ""
        final_tokens = 0
        print(f"param_list: {param_list}")
        for param in param_list:
            print(f"param: {param}")
            content, completion_tokens = self.tool_call_function(conversation_id, task_id, param[0], param[1])
            final_content += f"""
tool: {param[0]}
result: {content}
"""
            final_tokens += completion_tokens

        if not final_content.startswith("@"):
            if self.pipeline and self.pipeline != "\\":
                receiver = self.pipeline
            else:
                receiver = self._storage_get_task_info(task_id)["par_agent_name"]
                if not receiver:
                    receiver = sender_name
            final_content = f"@{receiver} " + final_content
        return final_content, final_tokens

    def _generate_process(self, conv_info: DialogueManager):
        pre_sender_name = conv_info.sender_name
        content = conv_info.content
        completion_tokens = conv_info.completion_tokens
        try:
            conv_info.init_message_before_generate(self.name, self.agent_type)

            # 生成回复内容
            if self.agent_type != "TOOL" and self.agent_type != "HUMAN":
                # 压缩历史任务对话记录
                safe_size = self.get_agent_llm_config.main_model_config.request_config.max_messages_tokens
                messages_safe_size, total_tokens = self._chat_messages_safe_size(conv_info.task_id, safe_size)

                # 构建 system 提示词
                if self.switch.default_consider_mode == "on" or ((self.switch.default_consider_mode == "auto" or self.switch.default_consider_mode is None) and "gpt-4" not in self.get_agent_llm_config.main_model_config.model):
                    # 构建深思 system 提示词
                    pre_node_id = ""
                    system_prompt = ""
                    consider_message = ConsiderPrompts(self.switch.default_language, self.switch.task_tag, self.name,
                                                       self._get_work_flow, self.workmates)
                    while True:
                        pre_node_id, idea, system_prompt, next_node_id = consider_message.build_prompt(pre_node_id, system_prompt)
                        if next_node_id == "":
                            break
                        messages = messages_safe_size.copy()
                        messages.append({'role': 'system', 'content': system_prompt})
                        request_data = ChatCompletionsRequest(messages, self.switch.default_stream_mode)
                        content, completion_tokens = generate_chat_completion(
                            self.get_agent_llm_config.main_model_config, request_data, conv_info, "idea", idea)
                        conv_info.content = content
                        conv_info.completion_tokens = completion_tokens
                        self.switch.storage and self.switch.storage.add_message(conv_info.conversation_id,
                                                                                conv_info.message("idea", idea))
                else:
                    # 构建普通 system 提示词
                    system_prompt = self._prompts.build_system_prompt()

                # 插入任务消息，用于保持 agent 专注度
                if conv_info.sender_type != "HUMAN":
                    focus_message, total_tokens = self._task_info_message(conv_info.task_id)
                    if focus_message:
                        messages_safe_size.insert(0, focus_message)

                # 插入 system 消息
                system_message = {'role': 'system', 'content': system_prompt}
                messages_safe_size.insert(0, system_message)

                # 生成回复
                request_data = ChatCompletionsRequest(messages_safe_size, self.switch.default_stream_mode)
                content, completion_tokens = generate_chat_completion(
                    self.get_agent_llm_config.main_model_config, request_data, conv_info, "main", "")
                conv_info.content = content
                conv_info.completion_tokens = completion_tokens
                if not content:
                    raise ValueError("Failed to generate content.")

            if content:
                # 防止模型 @ 自己
                content = content.replace(f"@{self.name} ", "")

            # 使用工具
            content_type = "main"
            content_tag = ""

            if (self.agent_type == "TOOL" or self.agent_type == "HUMAN") or (self.agent_type == "TOOLMAN" and not content.startswith("@")):
                if self.agent_type == "TOOLMAN":
                    self.switch.storage and self.switch.storage.add_message(conv_info.conversation_id,
                                                                            conv_info.message("main", ""))
                param_list, start_tag, end_tag = self.tool_parameter_identification(content)
                conv_info.response(0, "tool", start_tag, "", 0, None)
                content, completion_tokens = self.tool_reply(conv_info.conversation_id, conv_info.task_id, pre_sender_name,
                                                             param_list)
                conv_info.response(1, "tool", start_tag, content, completion_tokens, None)
                conv_info.response(2, "tool", end_tag, '[DONE]', 0, None)

                content_type = "tool"
                content_tag = end_tag
            self.storage_add_compressed_message(conv_info)
            conv_info.before_switch(content, completion_tokens)
            self.switch.handle_and_forward(conv_info, content_type, content_tag)
        except SystemExit:
            print("The task is finished.")
        except Exception as e:
            print(f"generate_process :{e}")
            if self.agent_type == "TOOL" or self.agent_type == "HUMAN":
                conv_info.init_message_before_alert(f"@{pre_sender_name} Generate error, Please trying again")
                self.switch.system_alert(conv_info)

    async def _a_generate_process(self, conv_info: DialogueManager):
        pre_sender_name = conv_info.sender_name
        content = conv_info.content
        completion_tokens = conv_info.completion_tokens
        try:
            conv_info.init_message_before_generate(self.name, self.agent_type)

            # 生成回复内容
            if self.agent_type != "TOOL" and self.agent_type != "HUMAN":
                # 压缩历史任务对话记录
                safe_size = self.get_agent_llm_config.main_model_config.request_config.max_messages_tokens
                messages_safe_size, total_tokens = self._chat_messages_safe_size(conv_info.task_id, safe_size)

                # 构建 system 提示词
                if self.switch.default_consider_mode == "on" or ((self.switch.default_consider_mode == "auto" or self.switch.default_consider_mode is None) and "gpt-4" not in self.get_agent_llm_config.main_model_config.model):
                    # 构建深思 system 提示词
                    pre_node_id = ""
                    system_prompt = ""
                    consider_message = ConsiderPrompts(self.switch.default_language, self.switch.task_tag, self.name,
                                                       self._get_work_flow, self.workmates)
                    while True:
                        pre_node_id, idea, system_prompt, next_node_id = consider_message.build_prompt(pre_node_id, system_prompt)
                        if next_node_id == "":
                            break
                        messages = messages_safe_size.copy()
                        messages.append({'role': 'system', 'content': system_prompt})
                        request_data = ChatCompletionsRequest(messages, self.switch.default_stream_mode)
                        content, completion_tokens = await a_generate_chat_completion(
                            self.get_agent_llm_config.main_model_config, request_data, conv_info, "idea", idea)
                        conv_info.content = content
                        conv_info.completion_tokens = completion_tokens
                        self.switch.storage and self.switch.storage.add_message(conv_info.conversation_id,
                                                                                conv_info.message("idea", idea))
                else:
                    # 构建普通 system 提示词
                    system_prompt = self._prompts.build_system_prompt()

                # 插入任务消息，用于保持 agent 专注度
                if conv_info.sender_type != "HUMAN":
                    focus_message, total_tokens = self._task_info_message(conv_info.task_id)
                    if focus_message:
                        messages_safe_size.insert(0, focus_message)

                # 插入 system 消息
                system_message = {'role': 'system', 'content': system_prompt}
                messages_safe_size.insert(0, system_message)

                # 生成回复
                request_data = ChatCompletionsRequest(messages_safe_size, self.switch.default_stream_mode)
                content, completion_tokens = await a_generate_chat_completion(
                    self.get_agent_llm_config.main_model_config, request_data, conv_info, "main", "")
                conv_info.content = content
                conv_info.completion_tokens = completion_tokens
                if not content:
                    raise ValueError("Failed to generate content.")

                if content:
                    # 防止模型 @ 自己
                    content = content.replace(f"@{self.name} ", "")

            # 使用工具
            content_type = "main"
            content_tag = ""
            if (self.agent_type == "TOOL" or self.agent_type == "HUMAN") or (self.agent_type == "TOOLMAN" and not content.startswith("@")):
                if self.agent_type == "TOOLMAN":
                    self.switch.storage and self.switch.storage.add_message(conv_info.conversation_id,
                                                                            conv_info.message("main", ""))
                param_list, start_tag, end_tag = self.tool_parameter_identification(content)
                await conv_info.a_response(0, "tool", start_tag, "", 0, None)
                content, completion_tokens = self.tool_reply(conv_info.conversation_id, conv_info.task_id,
                                                             pre_sender_name, param_list)
                await conv_info.a_response(1, "tool", start_tag, content, completion_tokens, None)
                await conv_info.a_response(2, "tool", end_tag, '[DONE]', 0, None)
                content_type = "tool"
                content_tag = end_tag
            self.storage_add_compressed_message(conv_info)
            conv_info.before_switch(content, completion_tokens)
            await self.switch.a_handle_and_forward(conv_info, content_type, content_tag)
        except SystemExit:
            print("The task is finished.")
        except Exception as e:
            print(f"generate_process :{e}")
            if self.agent_type == "TOOL" or self.agent_type == "HUMAN":
                conv_info.init_message_before_alert(f"@{pre_sender_name} Generate error, Please trying again")
                await self.switch.a_system_alert(conv_info)
