import re
from collections import defaultdict
from typing import Optional, Dict

from autogan.tools.code_execution_tool import CodeExecution

from autogan.tools.wolfram_alpha_tool import WolframAlphaAPIWrapper

from autogan.oai.count_tokens_utils import count_text_tokens

from autogan.agents.universal_agent import UniversalAgent
from autogan.utils.compressed_text_utils import compressed_text_universal
from autogan.tools.web_search_tool import WebSearch


class ToolAgentSearch(UniversalAgent):
    def __init__(
            self,
            search_config: Dict,
            agent_config: Optional[Dict] = None,
            retry_times: Optional[int] = 10,
            name: Optional[str] = "WebSearchExp",
            duty: Optional[str] = 'Not only can I search for information on the internet, '
                                  'but I can also answer questions using the Wolfram engine.',
            work_flow: Optional[str] = """I hope you are an internet search expert. When you receive a search request, you have the following two tools to choose from:

1. web: You can search for information on the internet. When using it, please enclose the search keywords in your output with the ```web\n ``` symbol, for example:
```web
Your search keywords
```

2. wolfram: You can use the Wolfram engine to help you calculate or query data related to Mathematics, finance, unit conversion, data analysis, science, geography, history, culture, movies, music, etc. 
When using it, please enclose the English question that Wolfram can understand in your output with the ```wolfram\n ``` symbol, for example:
```wolfram
one wolfram query
```

Note: When you decide to use a tool, please do not @ anyone.""",
            # duty: Optional[str] = '我不但可以从网络上搜索资料，还可以通过 wolfram 引擎来回答问题。',
            #             work_flow: Optional[str] = """我希望你是一个网络搜索专家，当你收到搜索请求时，你有一下两种工具可供选择：
            #
            #  1. web: 可以在网络上查找资料。使用时请在你的输出内容中，将搜索关键词用```web\n ``` 符号封装，例如：
            # ```web
            # Your search keywords
            # ```
            #
            # 2.wolfram: 可以使用wolfram引擎，帮你计算或查询数学、金融、单位转换、数据分析、科学、地理、历史、文化、电影、音乐等相关数据。使用时请在你的输出内容中，将 wolfram 可以理解的英文问题用```wolfram\n ``` 符号封装，例如：
            # ```wolfram
            # one wolfram query
            # ```
            #
            # 注意：当你决定使用工具时，请不要@任何人""",
    ):
        """WebSearchExpert

        1.Receive the user's question and convert it into search keywords.

        2.Call the Google Search API to obtain a result and extract the webpage content.

        3.If no content related to the user's question is extracted,
        call the Google Search API again to obtain the next result.

        4.Repeat operations 2 and 3 until reaching retry_times.

        Within the same task session domain, if the search keywords are the same,
        the offset of the search results will accumulate and move backwards.

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
        :param search_config: JSON format of email_config {"cx": "", "key": ""}
        :param retry_times: Represent the maximum number of attempts for each search, the default is 10.
        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        :param work_flow: Defines the workflow of the agent.
            定义 agent 的工作流程。
        """
        super().__init__(
            name,
            agent_config=agent_config,
            duty=duty,
            work_flow=work_flow,
            use_tool="join"
        )
        self._web_search = WebSearch(search_config["google_search"]) if "google_search" in search_config else None
        self._wolfram_alpha = WolframAlphaAPIWrapper(
            search_config["wolfram_alpha"]) if "wolfram_alpha" in search_config else None
        self._conversation_search_index = defaultdict(int)
        self._retry_times = retry_times

    def tool_function(self, task_id: str, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        lang, code = CodeExecution.extract_code(param)
        if lang == "web" and code:
            if self._web_search:
                return self._web_function(task_id, code)
            else:
                return "Please add the Google Custom Search JSON API configuration.", 0
        elif lang == "wolfram" and code:
            if self._wolfram_alpha:
                return self._wolfram_alpha_function(code)
            else:
                return "Please add the WolframAlphaAPI configuration.", 0
        else:
            return """Please make a choice between web and wolfram, and use the ``` symbol for encapsulation, for example:
```wolfram
one wolfram query
```""", 18

    def _web_function(self, task_id: str, param: str) -> tuple[str, int]:
        loop = self._retry_times
        for i in range(loop):
            # Accumulate the search offset of the same task and the same keyword.
            self._conversation_search_index[task_id] += 1
            start = self._conversation_search_index[task_id]

            # Get webpage content.
            detail = self._web_search.get_search_detail(param, start, self.name, "search", self.response_func)

            if detail:
                # Extract content related to the user's question from the webpage content.
                compressed_text, total_tokens = compressed_text_universal(
                    detail, self.agent_config.summary_model_config, self.name, self.response_func, self.stream_mode,
                    self._conversation_focus[task_id],
                    self.agent_config.summary_model_config.max_messages_tokens)
                if compressed_text:
                    return compressed_text, total_tokens
            if i == loop - 1:
                return "No useful content was found this time. If necessary, I can continue searching for you.", 18

    def _wolfram_alpha_function(self, param: str) -> tuple[str, int]:
        # Extract Wolfram questions from the text generated by LLM.
        pattern = "```wolfram\n(.*?)```"
        param = re.search(pattern, param, re.DOTALL).group(1)

        # Call wolfram alpha api
        reply = self._wolfram_alpha.run(param)
        if reply:
            tokens = count_text_tokens(reply)
            return reply, tokens
        else:
            return "Request failed, you can choose to retry", 8
