from typing import Optional, Dict, List

from autogan.tools.code_execution_tool import CodeExecution
from autogan.utils.compressed_texts_utils import compressed_texts

from autogan.utils.json_utils import text_to_json

from autogan.agents.universal_agent import UniversalAgent
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.tools.file_tool import File


class ToolAgentDocument(UniversalAgent):
    def __init__(
            self,
            agent_llm_config: Optional[Dict] = None,
            name: Optional[str] = "DocumentExp",
            duty: Optional[str] | Optional[dict] = None,
            work_flow: Optional[str] | Optional[dict] = None,
            # duty: Optional[str] = '我是文件助手，可以帮你打开本地的word、excel、pdf 文件，还可以向 docx 文件的结尾追加新的内容。',
            #             work_flow: Optional[str] = """我希望你是一个文件助手，当你收到有关打开文件或追加内容的请求时，不用管你自身是否有能力实现，因为你有一下两种工具可供选择：
            #
            #  1. 阅读器: 可以打开 word、excel、pdf 文件。使用方式如下：
            # ```reader
            # 带扩展名的文件名
            # ```
            #
            # 2.写入器: 可以向 docx 文件的结尾追加新的内容，使用方式如下：
            # ```append
            # {"file_name": "不带扩展名的文件名称", "text": "待追加的文本内容"}
            # ```
            #
            # 注意：当你决定使用工具时，请不要@任何人""",
            work_dir: Optional[str] = None,

    ):
        """FileReadExpert

        Open Word, Excel, PDF documents and return their contents.

        Receive file names with extensions.

        :param agent_llm_config: The agent configuration includes:
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
        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        :param work_flow: Defines the workflow of the agent.
            定义 agent 的工作流程。
        :param work_dir: The relative path of the document, default is extensions
        """
        duty = duty if duty else {
            "EN": """I can view files uploaded by users and tell you what I see in the content. However, I need to know the exact file name (including the extension) and the specific question you have (For example: legal review, the main content of the document, the process of car insurance reporting, etc).""",
            "CN": """我可以查看用户上传的文件，并将我看到的内容告诉你。但我需要知道准确的文件名称（包括扩展名）还有你要了解的问题（例如：进行法律审核、文件的主要内容、车险报案的流程等）"""
        }

        work_flow = work_flow if work_flow else {
            "EN": """There are three tools available to help you review user-uploaded files. Please choose one based on the situation:

1. summary: This tool provides answers by analyzing the entire content of the file, For example: contract review, extract the main content of the document, etc. but it consumes a lot of resources. When using it, please output in JSON format {"file": "filename (including extension)", "question": "the question you want to know"}, and add the summary symbol, for example:
```summary
{"file": "test.pdf", "question": "Please review this contract"}
```

2. search: This tool allows you to first search for relevant content within the file and then summarize it, using much fewer resources. When using it, please output in JSON format {"file": "filename (including extension)", "question": "the question you want to know"}, and add the search symbol, for example:
When using it, please enclose the English question that Wolfram can understand in your output with the ```wolfram\n ``` symbol, for example:
```search
{"file": "test.pdf", "question": "What is the process for filing a car insurance claim?"}
```

Note: When you decide to use a tool, please do not @ anyone.""",
            "CN": """这里有三个工具，可以帮你查看用户上传的文件，请根据实际情况进行选择:
1. summary:这个工具通过分析完整的文件内容给出答案，例如：合同审核，提炼文件主要内容等。但是会消耗很多资源。使用时请输出json格式{"file": "文件名（包括扩展名）", "question": "需要了解的问题"}，并加上 summary 符号，例如:
```summary
{"file": "test.pdf", "question": "审核下这份合同"}
```

2. search:这个工具可以先从文件中查询出相关内容在进行总结，消耗的资源很小。使用时请输出json格式{"file": "文件名（包括扩展名）", "question": "需要了解的问题"}，并加上 search 符号，例如:
```search
{"file": "test.pdf", "question": "车险报案的流程是？"}
```

3. excel:这是一个处理 excel 的专用工具，对于 excel 文件的相关请求请使用此工具。使用时请输出json格式{"file": "文件名（包括扩展名）", "question": "需要了解的问题"}，并加上 excel 符号，例如:
```search
{"file": "test.xlsx", "question": "销售额的变化趋势是？"}
```

注意:当您决定使用某个工具时，请不要@任何人。"""
        }
        super().__init__(
            name,
            agent_llm_config=agent_llm_config,
            duty=duty,
            work_flow=work_flow,
            agent_type="TOOLMAN"
        )
        self._file = File(work_dir)

    def tool_parameter_identification(self, content: Optional[str] = None) -> tuple[List[tuple], str, str]:
        param_list = CodeExecution.extract_code(content)
        return param_list, "Searching", "File content"

    def tool_call_function(self, conversation_id: int, task_id: int, tool: str, param: str | dict) -> tuple[str, int]:
        param = text_to_json(param)
        if param and tool == "summary" and param:
            texts = self.switch.es.get_chat_file_pack(conversation_id, param["file"], 40)
        elif param and tool == "search" and param:
            texts = self.switch.es.get_chat_file_hybrid(conversation_id, param["file"], param["question"])
        elif param and tool == "excel" and param:
            texts = self.switch.es.get_chat_file_pack(conversation_id, param["file"], 40)
        else:
            return """Search failure""", 18
        return self._summary_function(texts, param["question"])

    def _summary_function(self, texts: list, focus: str) -> tuple[str, int]:
        text, token = compressed_texts(self.switch.default_language, texts, self.get_agent_llm_config.summary_model_config,
                                       focus,
                                       self.get_agent_llm_config.summary_model_config.request_config.max_messages_tokens)
        if text and token:
            return text, token
        else:
            return 'No relevant content found', 3
