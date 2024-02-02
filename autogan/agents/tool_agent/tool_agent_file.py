from typing import Optional, Dict

from autogan.tools.code_execution_tool import CodeExecution

from autogan.utils.json_utils import text_to_json

from autogan.agents.universal_agent import UniversalAgent
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.tools.file_tool import File


class ToolAgentFile(UniversalAgent):
    def __init__(
            self,
            agent_config: Optional[Dict] = None,
            name: Optional[str] = "FileReadExp",
            duty: Optional[
                str] = 'I am a document assistant, capable of helping you open local Word, Excel, and PDF files, and also able to append new content to the end of DOCX files.',
            work_flow: Optional[str] = """I hope you are a document assistant. When you receive requests related to opening files or appending content, regardless of your own capabilities, you have the following two tools to choose from:

1. reader: Can open Word, Excel, and PDF files. The usage is as follows:
```reader
Filename with extension
```

2. append: Can append new content to the end of a DOCX file. The usage is as follows:
```append
{"file_name": "File name without extension", "text": "Text to be appended"}
```

Note: When you decide to use a tool, please do not @ anyone.""",
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
        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        :param work_flow: Defines the workflow of the agent.
            定义 agent 的工作流程。
        :param work_dir: The relative path of the document, default is extensions
        """
        super().__init__(
            name,
            agent_config=agent_config,
            duty=duty,
            work_flow=work_flow,
            agent_type="TOOLMAN"
        )
        self._file = File(work_dir)

    def tool_filter(self, param: Optional[str] = None) -> tuple[str, str, str, str]:
        lang, code = CodeExecution.extract_code(param)
        if lang == "reader" and code:
            return lang, code, "Opening", "File content"
        elif lang == "append" and code:
            return lang, code, "Opening", "File content"
        else:
            return "", "", "Opening", "File content"

    def tool_function(self, conversation_id: int, task_id: int, lang: Optional[str] = None, code: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        if lang == "reader" and code:
            return self._reader_function(code)
        elif lang == "append" and code:
            return self._append_function(code)
        else:
            return """Please make a choice between reader and append, and use the ``` symbol for encapsulation, for example:
        ```reader
        Filename with extension
        ```""", 18

    def _reader_function(self, param: str) -> tuple[str, int]:
        text = self._file.read(param)
        if text is not None and text != "":
            tokens = count_text_tokens(text)
            return text, tokens
        else:
            print("False")
            return 'File opening failure', 3

    def _append_function(self, param: str) -> tuple[str, int]:
        param = text_to_json(param)
        if param:
            reply = self._file.append_to_word(param['file_name'], param['text'])

            if reply:
                param = f"Text appended successfully, saved to: {param['file_name']}.docx"
                tokens = count_text_tokens(param)
                return param, tokens

        return ('Failed to append the text, please ensure the text to be appended is sent in the '
                'format of {"file_name": "file name without extension", "text": "text to be '
                'appended"}.'), 39
