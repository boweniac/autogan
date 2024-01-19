import os
from typing import Optional, Dict


class ConfigList:
    def __init__(
            self,
            config_list,
    ):
        self._config_list = config_list
        self.index = 0

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
    def len(self) -> int:
        """The length of the configuration list.
        """
        return len(self._config_list)


class AudioSpeechRequestConfig:
    def __init__(
            self,
            request_interval_time: Optional[int] = None,
            request_timeout: Optional[int] = None,
            max_retries: Optional[int] = None,
            work_dir: Optional[str] = None,
    ):
        self.request_interval_time = request_interval_time if request_interval_time else 0
        self.request_timeout = request_timeout if request_timeout else 120
        self.max_retries = max_retries if max_retries else 3
        work_dir = work_dir if work_dir else "extensions"
        absolute_work_dir = os.getcwd() + f"/{work_dir}/"
        os.makedirs(f"{absolute_work_dir}", exist_ok=True)
        self.work_dir = absolute_work_dir


class AudioSpeechConfig:
    """LLM config object
    """

    def __init__(
            self,
            config: Dict,
    ):
        self._api_key_list = ConfigList(config["api_key_list"])
        self._request_config = AudioSpeechRequestConfig(
            config["request_interval_time"],
            config["request_timeout"],
            config["max_retries"],
            config["work_dir"]
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
    def request_config(self):
        return self._request_config
