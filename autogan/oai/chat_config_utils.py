from typing import Optional, Dict


class ConfigList:
    def __init__(
            self,
            config_list,
            model_filter: Optional[str] = None,
    ):
        self._config_list = self._config_filter(config_list, model_filter)
        self.index = 0

    @staticmethod
    def _config_filter(config_list, model_filter: Optional[str] = None) -> list:
        if model_filter:
            filter_list = []
            for config in config_list:
                if model_filter in config["model"]:
                    filter_list.append(config)
            return filter_list
        else:
            return config_list

    def get_config(self, index) -> Dict:
        """Get the one configuration in the configuration list.
        """
        config = self._config_list[index]
        return config

    @property
    def get_next_config(self) -> Dict:
        """Get the next configuration in the configuration list.
        """
        config = self._config_list[self.index]
        self.index = (self.index + 1) % len(self._config_list)
        return config

    @property
    def get_first_config(self) -> Dict:
        """Get the first configuration in the configuration list.
        """
        return self._config_list[0]

    @property
    def len(self) -> int:
        """The length of the configuration list.
        """
        return len(self._config_list)


class AgentLLMConfig:
    """The agent configuration includes:
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
    """

    def __init__(
            self,
            config: Dict,
    ):
        # main model config
        self._main_model_api_key_list = ConfigList(config["main_model"]["api_key_list"],
                                                   config["main_model"].get("model_filter"))
        self._main_model_max_messages_tokens = config["main_model"].get("max_messages_tokens")

        # summary model config
        if "summary_model" in config:
            self._summary_model_api_key_list = ConfigList(config["summary_model"]["api_key_list"],
                                                          config["summary_model"].get("model_filter"))
            self._summary_model_max_messages_tokens = config["summary_model"].get("max_messages_tokens")
        else:
            # Use the main_model configuration when the summary_model configuration is empty.
            self._summary_model_api_key_list = self._main_model_api_key_list
            self._summary_model_max_messages_tokens = self._main_model_max_messages_tokens

        self._request_interval_time = config.get("request_interval_time")
        self._request_timeout = config.get("request_timeout")
        self._max_retries = config.get("max_retries")
        self._max_conv_turns = config.get("max_conv_turns")

    @property
    def main_model_config(self):
        return LLMConfig(
            self._main_model_api_key_list,
            self._main_model_max_messages_tokens,
            self._request_interval_time,
            self._request_timeout,
            self._max_retries,
            self._max_conv_turns
        )

    @property
    def summary_model_config(self):
        return LLMConfig(
            self._summary_model_api_key_list,
            self._summary_model_max_messages_tokens,
            self._request_interval_time,
            self._request_timeout,
            self._max_retries,
            self._max_conv_turns
        )


class LLMRequestConfig:
    def __init__(
            self,
            max_messages_tokens: Optional[int] = None,
            request_interval_time: Optional[int] = None,
            request_timeout: Optional[int] = None,
            max_retries: Optional[int] = None,
            max_conv_turns: Optional[int] = None,
    ):
        self.max_messages_tokens = max_messages_tokens if max_messages_tokens else 4096
        self.request_interval_time = request_interval_time if request_interval_time else 0
        self.request_timeout = request_timeout if request_timeout else 120
        self.max_retries = max_retries if max_retries else 3
        self.max_conv_turns = max_conv_turns if max_retries else 20


class LLMConfig:
    """LLM config object
    """

    def __init__(
            self,
            api_key_list: ConfigList,
            max_messages_tokens: Optional[int] = None,
            request_interval_time: Optional[int] = None,
            request_timeout: Optional[int] = None,
            max_retries: Optional[int] = None,
            max_conv_turns: Optional[int] = None,
    ):
        self._api_key_list = api_key_list
        self._request_config = LLMRequestConfig(
            max_messages_tokens,
            request_interval_time,
            request_timeout,
            max_retries,
            max_conv_turns
        )

    def api_key(self, index):
        """Get the one configuration in the api_key_list.
        """
        return self._api_key_list.get_config(index)

    @property
    def next_api_key(self):
        """Get the next configuration in the api_key_list.
        """
        return self._api_key_list.get_next_config

    @property
    def len_of_api_key_list(self) -> int:
        """Get the first configuration in the api_key_list list.
        """
        return self._api_key_list.len

    @property
    def model(self):
        """Get the model of the first configuration in the api_key_list list.
        """
        return self._api_key_list.get_first_config["model"]

    @property
    def request_config(self):
        return self._request_config
