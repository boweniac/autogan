from collections import defaultdict

# from autogan.prompt.agent import consider_prompts
from autogan.utils.environment_utils import environment_info

from autogan.oai.chat_api_utils import ChatCompletionsRequest
from autogan.oai.chat_config_utils import LLMConfig
from autogan.oai.chat_generate_utils import generate_chat_completion_internal

consider_prompts = {
    "node_1": {
        "type": "idea",
        "next_id": "node_2",
        "content": {
            "CN": {
                "idea": "反思之前的对话是否陷入循环或遇到困难",
                "prompt": """# 任务：请分析上述对话记录。特别关注以下几点：
## 分析前应先了解: 
### 你在群聊中的角色：${agent_name}

### 你的预设工作流:
${work_flow}

## 分析需求:
### 分析需求 1: 对话记录中是否出现死循环，例如：双方不断重复进行相同的请求与回复。
### 分析需求 2: 你在执行工作流时，是否遇到了困难。

## 分析结果输出要求:
### 如果遇到死循环或困难: 请站在 ${agent_name} 的角度提出如何脱离死循环或解决困难。
### 如果上述对话记录没有问题: 请仅输出一个单词 'None'"""
            },
            "EN": {
                "idea": "Reflect on whether the previous conversation has fallen into a loop or encountered difficulties.",
                "prompt": """# Task: Please analyze the conversation log above. Pay special attention to the following points:
## Before analyzing, it is necessary to understand:
### Your role in the group chat: ${agent_name}

### Your preset workflow:
${work_flow}

## Analysis Requirements:
### Analysis Requirement 1: Whether there is a loop in the conversation log, for example, both sides keep repeating the same requests and replies.
### Analysis Requirement 2: Whether you encountered any difficulties while executing the workflow.

## Analysis Result Output Requirements:
### If you encounter a loop or difficulty: Please, from the perspective of ${agent_name}, suggest how to break the loop or solve the difficulty.
### If there are no issues in the conversation log: Please just output the word 'None'"""
            }
        }
    },
    "node_2": {
        "type": "idea",
        "next_id": "node_3",
        "content": {
            "CN": {
                "idea": "思考下一步需要做什么",
                "prompt": """# 任务：请分析上述对话记录。特别关注以下几点：
## 分析前应先了解: 
### 你在群聊中的角色：${agent_name}

### 你的预设工作流:
${work_flow}

### 对于接下来工作的一些建议
${node_1}

## 分析需求:
### 分析需求 1: 在下一次回复的内容中，需要着重完成工作流中的哪一项？

## 分析结果输出要求:
### 要求 1: 请输出在下一次回复中，你需要做的具体工作(所有需要考虑的细节，包括推荐的方法或工具等)。
### 要求 2: 请忽略已完成的工作。
### 要求 3: 请讲工作内容限定为下次回复可以完成的范围。"""
            },
            "EN": {
                "idea": "Think about what to do next",
                "prompt": """# Task: Please analyze the conversation log above. Pay special attention to the following points:
## Before analyzing, it is necessary to understand:
### Your role in the group chat: ${agent_name}

### Your preset workflow:
${work_flow}

### Suggestions for Upcoming Work:
${node_1}

## Analysis Requirements:
### Requirement 1: In your next response, which part of the workflow needs to be emphasized?

## Analysis Result Output Requirements:
### Requirement 1: Please specify the exact work you need to do in your next reply (including all the details to consider, recommended methods or tools, etc.).
### Requirement 2: Please ignore any work that has been completed.
### Requirement 3: Please ensure the work content is limited to what can be accomplished in the next reply."""
            }
        }
    },
    "node_3": {
        "type": "idea",
        "next_id": "node_4",
        "content": {
            "CN": {
                "idea": "思考接下来要与谁交流",
                "prompt": """# 任务：请分析上述对话记录。特别关注以下几点：
## 分析前应先了解: 
### 你的下一步工作:
${node_2}

### 其他可以帮助你的助手 (包括他们能做什么和不能做什么):
${workmates}

## 分析需求:
### 分析需求 1: 根据你的工作内容分析谁是你下一次回复需要交流的助手 (注意你只能选择一个助手)

## 分析结果输出:
### 输出 1: 哪一个是你下一次回复需要交流的助手？。
### 输出 2: 对方接收消息时有哪些要求。
### 输出 3: 对方能做哪些事情？。
### 输出 4: 对方不能做哪些事情？。

注:请提供正确的助手名称，不要提供不存在的名称。"""
            },
            "EN": {
                "idea": "Think about who to communicate with next",
                "prompt": """# Task: Please analyze the conversation log above. Pay special attention to the following points:
## Before analyzing, it is necessary to understand:
### Your next step of work:
${node_2}

### Other assistants that can help you (including what they can and cannot do):
${workmates}

## Analysis Requirements:
### Requirement 1: Based on the content of your work, analyze who is the next assistant you need to communicate with for your reply (note you can only choose one assistant)

## Analysis Result Output:
### Output 1: Which assistant do you need to communicate with for your next reply?
### Output 2: What are the requirements when the other party receives the message?
### Output 3: What can the other party do?
### Output 4: What can't the other party do?

* Note: Please provide the correct name of the assistant, do not provide names that do not exist."""
            }
        }
    },
    "node_4": {
        "type": "idea",
        "next_id": "node_5",
        "content": {
            "CN": {
                "idea": "总结接下来应如何回复",
                "prompt": """# 任务：请分析上述对话记录。特别关注以下几点：
## 分析前应先了解: 
### 当前时间: ${current_time}

### 你在群聊中的角色：${agent_name}

### 你的下一步工作:
${node_2}

### 你下一步需要交流的助手:
${node_3}

## 分析结果输出要求:
### 要求 1: 回复内容必须以 @+助手名称 开头，例如: @SearchExpert ${task_tag} 请帮我搜索2024年奥斯卡奖名单。
### 要求 2: 每次回复只能 @ 一名助手，否则对方不会收到你的消息。
### 要求 3: 在寻求帮助时，您需要先发布一个任务，方法是:@+助手名称+' '+${task_tag}+' '+任务内容，例如: @SearchExpert ${task_tag} 请帮我搜索2024年奥斯卡奖名单。
### 要求 4: 其他的助手无法看到任务发布前的对话记录，而且也无法看到你和其他人的对话记录"""
            },
            "EN": {
                "idea": "Summary How to respond next",
                "prompt": """# Task: Please analyze the conversation log above. Pay special attention to the following points:
## Before analyzing, it is necessary to understand:
### Current time: ${current_time}

### Your role in the group chat: ${agent_name}

### Your next task:
${node_2}

### The assistant you need to communicate with next:
${node_3}

## Analysis Result Output Requirements:
### Requirement 1: Replies must start with @+assistant's name, for example: @SearchExpert ${task_tag} please help me search for the 2024 Oscar nominees list.
### Requirement 2: Each reply can only @ one assistant, otherwise the other party will not receive your message.
### Requirement 3: When seeking help, you need to first post a task by saying: @+assistant's name+' '+${task_tag}+' '+task content，for example: @SearchExpert ${task_tag} please help me search for the 2024 Oscar nominees list.。
### Requirement 4: Other assistants cannot see the conversation history before the task was posted, nor can they see your conversation with others."""
            }
        }
    }
}


class UniversalAgentPrompt:
    def __init__(self, agent_name: str, work_flow: str, lang: str, task_tag: str, workmates: str, pipeline: str):
        self._agent_name = agent_name
        self._work_flow = work_flow
        self._lang = lang
        self._task_tag = task_tag
        self._workmates = workmates
        self._pipeline = pipeline

    def base_message_system_prompt(self) -> str:
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

    def base_message_focus_prompt(self, task_publisher, task_content) -> str:
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

        return focus_prompt


class ConsiderMessage:
    def __init__(self, lang: str, task_tag: str, agent_name: str, work_flow: str, workmates: str):
        self._lang = lang
        self._agent_name = agent_name
        self._work_flow = work_flow
        self._task_tag = task_tag
        self._workmates = workmates
        self._replace = {}
        self._init_replace()

    def _init_replace(self):
        self._replace["current_time"] = environment_info()
        self._replace["agent_name"] = self._agent_name
        self._replace["work_flow"] = self._work_flow
        self._replace["task_tag"] = self._task_tag
        self._replace["workmates"] = self._workmates

    def next_prompt(self, pre_id: str, pre_result: str, id: str) -> tuple[str, str, str, str]:
        if pre_id:
            self._replace[pre_id] = pre_result
        next_id: str = consider_prompts[id]["next_id"]
        idea: str = consider_prompts[id]["content"][self._lang]["idea"]
        prompt_str: str = consider_prompts[id]["content"][self._lang]["prompt"]
        prompt = self.replace(prompt_str)
        return id, idea, prompt, next_id

    def replace(self, text) -> str:
        print(f"self._replace: {self._replace}")
        for key, value in self._replace.items():
            print(f"${{{key}}}")
            text = text.replace(f"${{{key}}}", value)
        return text

    # def replace
