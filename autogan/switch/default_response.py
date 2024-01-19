from typing import Optional

from autogan.protocol.response_protocol import ResponseProtocol

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x


class DefaultResponse(ResponseProtocol):
    def __init__(self):
        self.conv_turns: int = 0
        self.req_msg_id: Optional[int] = None

    def send(self, msg_id: int, task_id: int, requester_name: str, index: int, content_type: str,
             content: str, completion_tokens: int, response: any):
        """default response function
        默认响应函数提供终端打印支持
        The default response function provides terminal printing support.

        :param msg_id:
        :param task_id:
        :param requester_name:
        :param index: response sequence
        :param content_type:
        :param content: completion content
        :param completion_tokens: completion tokens
        :param response: Respond to raw data
        :return:
        """
        if index > 0:
            end = ""
        else:
            end = "\n"

        if content:
            if content_type == "main":
                if index == 1:
                    print(f"\n{requester_name}: ", end=end)
                print(content, end=end)
            elif content_type == "idea" or content_type == "tool_call":
                if index == 1:
                    print(
                        colored(
                            f"\n{requester_name}: ",
                            "cyan",
                        ),
                        end=end,
                        flush=True,
                    )
                print(
                    colored(
                        content,
                        "cyan",
                    ),
                    end=end,
                    flush=True,
                )
            elif content_type == "system":
                print(
                    colored(
                        f"\n{requester_name}: {content}",
                        "red",
                    ),
                    end=end,
                    flush=True,
                )
            elif content_type == "tool":
                print(
                    colored(
                        f"\n{requester_name}: {content}",
                        "blue",
                    ),
                    end=end,
                    flush=True,
                )
            elif content_type == "search":
                print(
                    colored(
                        f"\nurl: {content}",
                        "cyan",
                    ),
                    end=end,
                    flush=True,
                )
