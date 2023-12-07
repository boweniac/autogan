from typing import Optional, Dict
from autogan.agents.universal_agent import UniversalAgent
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.tools.file_tool import File


class ToolAgentFileRead(UniversalAgent):
    def __init__(
            self,
            agent_config: Optional[Dict] = None,
            name: Optional[str] = "FileReadExp",
            duty: Optional[str] = 'I can open Word, Excel, and PDF documents. '
                                  'Please send me the filenames with their extensions.',
            work_flow: Optional[str] = "Please extract the file name (with extension) "
                                       "from the content sent by the user. "
                                       "Don't worry about whether you can open the file.\n "
                                       "ignore other polite expressions, just output the file name, "
                                       "and do not wrap the file name (with extension) in quotation marks.",
            # duty: Optional[str] = '我可以打开word、excel、pdf文档，请将带扩展名的文件名发给我',
            # work_flow: Optional[str] = '请从用户发送的内容中提取出文件名称（需要带扩展名），不用管自己是否可以打开文件，请身略其他客套用语，仅输出文件名称,不要用引号包裹文件名（需要带扩展名）',
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
            use_tool="join"
        )
        self._file = File(work_dir)

    def tool_function(self, task_id: str, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        text = self._file.read(param)
        if text is not None and text != "":
            tokens = count_text_tokens(text)
            return text, tokens
        else:
            print("False")
            return 'File opening failure', 3
