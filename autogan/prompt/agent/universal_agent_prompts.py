from collections import defaultdict

from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.utils.environment_utils import environment_info


class UniversalAgentPrompt:
    def __init__(self, lang: str, task_tag: str, agent_name: str, work_flow: str, workmates: str, pipeline: str):
        """该类用于构建 system 提示词和任务提示词，其中任务其实词用于 agent 在任务执行过程中保持专注度，不管对话记录如何压缩，任务其实词都不会改变

        :param lang: 语言
        :param task_tag: 任务关键词，agent 可用其创建任务
        :param agent_name: agent 名称
        :param work_flow: 工作流
        :param workmates: 可协作的其他 agent 和相关介绍
        :param pipeline: 工作流模式中，下一个衔接的 agent 名称"""

        self._agent_name = agent_name
        self._work_flow = work_flow
        self._lang = lang
        self._task_tag = task_tag
        self._workmates = workmates
        self._pipeline = pipeline
        self._task_tokens = defaultdict(int)

    def build_system_prompt(self) -> str:
        """构建 system 提示词"""
        current_time = environment_info()
        if self._lang == "CN":
            system_prompt = f"""# 角色:
在群聊中你的名字叫 {self._agent_name}，是一个注重效率且不会轻言放弃的助手。在对话中你不需要向其他人解释你的计划或说一些感谢之类的话，回复内容应当以推进工作为主。

# 工作:
## 工作流程 (请遵循以下流程完成你的工作):
{self._work_flow}

## 其他助手 (你可以向其他助手求助):
{self._workmates}

## 相关信息
### 当前时间: {current_time}

# 规则 (回复时请遵守以下规则):
## 规则 1: 回复内容必须以 @+助手名称 开头，例如: @SearchExpert {self._task_tag} 请帮我搜索2024年奥斯卡奖名单。
## 规则 2: 每次回复只能 @ 一名助手，否则对方不会收到你的消息。
## 规则 3: 在寻求帮助时，您需要先发布一个任务，方法是:@+助手名称+' '+{self._task_tag}+' '+任务内容，例如: @SearchExpert {self._task_tag} 请帮我搜索2024年奥斯卡奖名单。
## 规则 4: 其他的助手无法看到任务发布前的对话记录，而且也无法看到你和其他人的对话记录"""

        else:
            system_prompt = f"""# Role:
In the group chat, your name is {self._agent_name}，and you are an assistant who focuses on efficiency and never gives up easily. In the conversation, you don't need to explain your plans to others or say things like thank you. Your responses should primarily focus on advancing the work.

# Work:
## Workflow (Please follow the following process to complete your work):
{self._work_flow}

## Other Assistants (You can ask other assistants for help):
{self._workmates}

## Related Information
### Current Time: {current_time}

# Rules (Please adhere to the following rules in your reply):
## Rule 1: Replies must start with @+assistant's name, for example: @SearchExpert {self._task_tag} please help me search for the 2024 Oscar nominees list.
## Rule 2: Each reply can only @ one assistant, otherwise the other party will not receive your message.
## Rule 3: When seeking help, you need to first post a task by saying: @+assistant's name+' '+{self._task_tag}+' '+task content，for example: @SearchExpert {self._task_tag} please help me search for the 2024 Oscar nominees list.。
## Rule 4: Other assistants cannot see the conversation history before the task was posted, nor can they see your conversation with others."""

        return system_prompt

    def build_focus_prompt(self, task_id: int, task_publisher, task_content) -> tuple[str, int]:
        """构建任务提示词，用于 agent 在任务执行过程中保持专注度，不管对话记录如何压缩，任务其实词都不会改变

        :param task_id: 任务 id
        :param task_publisher: 任务发布者
        :param task_content: 任务内容"""
        if self._lang == "CN":
            focus_prompt = f"""# 当前任务:
## 任务内容
{task_content}

## 任务发布者
{task_publisher}

## 任务提交"""
            if self._pipeline and self._pipeline != "\\":
                focus_prompt += f"""
当你完成任务后，请将最终结果提交给 {self._pipeline}，例如: @{self._pipeline} {self._task_tag} ...。"""
            else:
                focus_prompt += f"""
当你完成任务后，请将最终结果提交给 {task_publisher}, 例如: @{task_publisher} ...。"""
        else:
            focus_prompt = f"""# Current Task
## Task Content
{task_content}

## Task Publisher
{task_publisher}

## Task Submission"""
            if self._pipeline and self._pipeline != "\\":
                focus_prompt += f"""
When you complete the task, please submit the final result to {self._pipeline}，For example: @{self._pipeline} {self._task_tag} The email has been successfully sent."""
            else:
                focus_prompt += f"""
When you complete the task, please submit the final result to {task_publisher}, For example: @{task_publisher} The email has been successfully sent."""

        if task_id in self._task_tokens:
            tokens = self._task_tokens[task_id]
        else:
            tokens = count_text_tokens(focus_prompt)
            self._task_tokens[task_id] = tokens

        return focus_prompt, tokens
