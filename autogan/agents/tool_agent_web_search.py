from collections import defaultdict
from typing import Optional, Dict
from autogan.agents.universal_agent import UniversalAgent
from autogan.utils.compressed_text_utils import compressed_text_universal
from autogan.tools.web_search_tool import WebSearch


class ToolAgentWebSearch(UniversalAgent):
    def __init__(
            self,
            search_config: Dict,
            agent_config: Optional[Dict] = None,
            retry_times: Optional[int] = 10,
            name: Optional[str] = "WebSearchExp",
            duty: Optional[str] = 'I can search for information online, but I can only search one website at a time. \n'
                                  'If my response is that I did not find useful content, '
                                  'it may be because the website is outdated and cannot be opened. \n'
                                  'To get useful answers, you might want to '
                                  'let me search multiple times (until I find useful content). \n'
                                  'Also, please do not post new tasks while I am still searching.',
            work_flow: Optional[str] = "I hope you are a keyword generator, "
                                       "generating a set of search keywords based on the task content. Please note:\n"
                                       "1.I don't need you to directly answer my question, "
                                       "let alone communicate with me, just output keywords.\n"
                                       "2.In the generated keywords, please do not include the current specific time.\n"
                                       "3.Don't worry about whether you have the ability to search, "
                                       "even if the keywords are the same, "
                                       "the website content queried each time is different.\n"
                                       "4.Please omit unnecessary polite language when replying, "
                                       "only output keywords, and separate keywords with spaces. "
                                       "Do not wrap keywords with quotes, etc. "
                                       "If there are special symbols in the keywords, please translate them.",
            # duty: Optional[str] = '我可以从网络上搜索资料，但是每次只能搜索一个网站，如果我的回复是没有搜索到有用的内容，'
            #                       '可能是因为网站过期无法打开，为了得到有用的答案建议可以让我多搜索几次（直至搜到有用的内容为止）。另外：继续搜索时请勿发布新的任务。',
            # work_flow: Optional[str] = '我希望你是一个关键词生成器，根据任务内容，生成一组搜索关键词。注意：\n'
            #                            '1.我不需要你直接回答我的问题，更不要和我交流，仅仅输出关键词。\n'
            #                            '2.生成的关键词中，请不要带有当前的具体时间。\n'
            #                            '3.不用担心自己是否有能力搜索，即便关键词相同，每次查询的也是不同的网站内容。\n'
            #                            '4.回复时请省略不必要的客套用语，仅输出关键词, 且关键词之间以空格分隔，关键词不要用引号等包裹，如关键词中带有特殊符号请转译。',
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
        self._conversation_search_index = defaultdict(int)
        self._web_search = WebSearch(search_config)
        self._retry_times = retry_times

    def tool_function(self, task_id: str, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
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
