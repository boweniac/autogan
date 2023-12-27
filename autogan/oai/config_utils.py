from typing import Optional, Dict


class ConfigList:
    def __init__(
            self,
            config_list,
            model_filter: Optional[str] = "",
    ):
        self._config_list = self._config_filter(config_list, model_filter)
        self.index = 0

    @staticmethod
    def _config_filter(config_list, model_filter) -> list:
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


class AgentConfig:
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
        model_filter = config["main_model"].get("model_filter", "")
        # main model config
        self._main_model_api_key_list = ConfigList(config["main_model"]["api_key_list"], model_filter)
        self._main_model_max_messages_tokens = config["main_model"]["max_messages_tokens"]

        # summary model config
        if "summary_model" in config:
            model_filter = config["summary_model"].get("model_filter", "")
            self._summary_model_api_key_list = ConfigList(config["summary_model"]["api_key_list"], model_filter)
            self._summary_model_max_messages_tokens = config["summary_model"]["max_messages_tokens"]
        else:
            # Use the main_model configuration when the summary_model configuration is empty.
            self._summary_model_api_key_list = self._main_model_api_key_list
            self._summary_model_max_messages_tokens = self._main_model_max_messages_tokens

        self._request_interval_time = config["request_interval_time"]
        self._request_timeout = config["request_timeout"]
        self._max_retries = config["max_retries"]
        self._max_conv_turns = config["max_conv_turns"] if "max_conv_turns" in config else None

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


class LLMConfig:
    """LLM config object
    """

    def __init__(
            self,
            api_key_list: ConfigList,
            max_messages_tokens: str,
            request_interval_time: int,
            request_timeout: int,
            max_retries: int,
            max_conv_turns: Optional[int]
    ):
        self._api_key_list = api_key_list
        self._max_messages_tokens = max_messages_tokens
        self._request_interval_time = request_interval_time
        self._request_timeout = request_timeout
        self._max_retries = max_retries
        self._max_conv_turns = max_conv_turns

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
    def max_messages_tokens(self):
        """Limit the maximum tokens of the context in each dialogue.
        """
        return self._max_messages_tokens

    @property
    def request_interval_time(self):
        return self._request_interval_time

    @property
    def request_timeout(self):
        return self._request_timeout

    @property
    def max_retries(self):
        return self._max_retries

    @property
    def max_conv_turns(self):
        return self._max_conv_turns
