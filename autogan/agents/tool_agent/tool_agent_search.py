import re
from collections import defaultdict
from typing import Optional, Dict, List

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
            agent_llm_config: Optional[Dict] = None,
            retry_times: Optional[int] = 10,
            name: Optional[str] = "WebSearchExp",
            duty: Optional[str] | Optional[dict] = None,
            work_flow: Optional[str] | Optional[dict] = None,
    ):
        """WebSearchExpert

        1.Receive the user's question and convert it into search keywords.

        2.Call the Google Search API to obtain a result and extract the webpage content.

        3.If no content related to the user's question is extracted,
        call the Google Search API again to obtain the next result.

        4.Repeat operations 2 and 3 until reaching retry_times.

        Within the same task session domain, if the search keywords are the same,
        the offset of the search results will accumulate and move backwards.

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
        :param search_config: JSON format of email_config {"cx": "", "key": ""}
        :param retry_times: Represent the maximum number of attempts for each search, the default is 10.
        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        :param work_flow: Defines the workflow of the agent.
            定义 agent 的工作流程。
        """
        duty = duty if duty else {
            "EN": """1. I can not only search for information on the internet. 2. I can use the Wolfram engine to answer questions 3. I can use the Wolfram engine to calculate formulas.""",
            "CN": """1. 我不但可以在网络上搜索信息。2. 可以利用 Wolfram engine 来回答问题。3. 可以利用 Wolfram engine 来计算公式"""
        }
        work_flow = work_flow if work_flow else {
            "EN": """I hope you are an internet search expert. When you receive a search request, you have the following two tools to choose from:

1. web: You can search for information on the internet. When using it, please enclose the search keywords in your output with the ```web\n ``` symbol, for example:
```web
Your search keywords 1
```

```web
Your search keywords 2
```

2. wolfram: You can use the Wolfram engine to help you calculate or query data related to Mathematics, finance, unit conversion, data analysis, science, geography, history, culture, movies, music, etc. 
When using it, please enclose the English question that Wolfram can understand in your output with the ```wolfram\n ``` symbol, for example:
```wolfram
one wolfram query 1
```

```wolfram
one wolfram query 2
```

Note: 
- When you decide to use a tool, please do not @ anyone.""",
            "CN": """我希望你是一个互联网搜索专家。当您收到搜索请求时，您有以下两个工具可供选择:
1. web:你可以在互联网上搜索信息。使用时，请在输出的搜索关键字中加上 web 符号，例如:
```web
你的搜索关键词 1
```

```web
你的搜索关键词 2
```
2. wolfram:您可以使用 wolfram 引擎来帮助您计算或查询与数学、金融、单位转换、数据分析、科学、地理、历史、文化、电影、音乐等相关的数据。
使用时，请在输出中附上 Wolfram 能理解的英文问题，并加上 Wolfram 符号，例如:
```wolfram
one wolfram query 1
```

```wolfram
one wolfram query 2
```

注意:
- 当您决定使用某个工具时，请不要@任何人。"""
        }
        super().__init__(
            name,
            agent_llm_config=agent_llm_config,
            duty=duty,
            work_flow=work_flow,
            agent_type="TOOLMAN"
        )
        self._web_search = WebSearch(search_config["google_search"]) if "google_search" in search_config else None
        self._wolfram_alpha = WolframAlphaAPIWrapper(
            search_config["wolfram_alpha"]) if "wolfram_alpha" in search_config else None
        self._conversation_search_index = defaultdict(int)
        self._retry_times = retry_times

    def tool_parameter_identification(self, content: Optional[str] = None) -> tuple[List[tuple], str, str]:
        param_list = CodeExecution.extract_code(content)
        return param_list, "Searching", "Search results"

    def tool_call_function(self, conversation_id: int, task_id: int, tool: str, param: str | dict) -> tuple[str, int]:
        if tool == "web" and param:
            if self._web_search:
                content, completion_tokens = self._web_function(task_id, param)
                return content, completion_tokens
            else:
                return "Please add the Google Custom Search JSON API configuration.", 0
        elif tool == "wolfram" and param:
            content_tag = ""
            content_tag_end = ""
            if self._wolfram_alpha:
                content, completion_tokens = self._wolfram_alpha_function(param)
                return content, completion_tokens
            else:
                return "Please add the WolframAlphaAPI configuration.", 0
        else:
            return """Please make a choice between web and wolfram, and use the ``` symbol for encapsulation, for example:
```wolfram
one wolfram query
```""", 18

    def _web_function(self, task_id: int, param: str) -> tuple[str, int]:
        loop = self._retry_times
        for i in range(loop):
            # Accumulate the search offset of the same task and the same keyword.
            self._conversation_search_index[task_id] += 1
            start = self._conversation_search_index[task_id]
            # Get webpage content.
            detail = self._web_search.get_search_detail(param, start)

            if detail:
                # Extract content related to the user's question from the webpage content.
                compressed_text, total_tokens = compressed_text_universal(self.switch.default_language,
                    detail, self.get_agent_llm_config.summary_model_config, self._task_info[task_id]['content'],
                    self.get_agent_llm_config.summary_model_config.request_config.max_messages_tokens)
                if compressed_text:
                    return compressed_text, total_tokens
            if i == loop - 1:
                return "No useful content was found this time. If necessary, I can continue searching for you.", 18

    def _wolfram_alpha_function(self, param: str) -> tuple[str, int]:
        # Extract Wolfram questions from the text generated by LLM.
        # pattern = "```wolfram\n(.*?)```"
        # print(param)
        # param = re.search(pattern, param, re.DOTALL).group(1)

        # Call wolfram alpha apps
        reply = self._wolfram_alpha.run(param)
        if reply:
            tokens = count_text_tokens(reply)
            return reply, tokens
        else:
            return "Request failed, you can choose to retry", 8
