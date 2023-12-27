from typing import Optional, Callable

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x

ResponseFuncType = Callable[[str, str, str, bool, int, Optional[str], Optional[int], any], None]


# def default_response_func(agent_name: str, gen: str, model: str, stream_mode: bool, index: int,
#                           content: Optional[str], tokens: Optional[int], response: any):
#     """default response function
#     默认响应函数提供终端打印支持
#     The default response function provides terminal printing support.
#
#     :param agent_name:
#     :param gen: Used to distinguish agent replies, deep thoughts, context compression, general summaries, clue summaries
#         用于区分 agent 回复、深思、压缩上下文、普通摘要、线索摘要
#         - main: agent replies
#         - idea: deep thoughts
#         - messages_summary: context compression
#         - text_summary: general summaries
#         - clue_summary: clue summaries
#         - system:
#         - tool:
#         - tool_call:
#     :param model:
#     :param stream_mode:
#     :param index: response sequence
#     :param content: completion content
#         生成内容
#     :param tokens: completion tokens
#         生成内容的 tokens
#     :param response: Respond to raw data
#         响应原始数据
#     :return:
#     """
#     if stream_mode:
#         end = ""
#     else:
#         end = "\n"
#
#     if content:
#         if gen == "main":
#             if index == 1:
#                 print(f"\n{agent_name}: ", end=end)
#             print(content, end=end)
#         elif gen == "idea" or gen == "tool_call":
#             if index == 1:
#                 print(
#                     colored(
#                         f"\n{agent_name}: ",
#                         "cyan",
#                     ),
#                     end=end,
#                     flush=True,
#                 )
#             print(
#                 colored(
#                     content,
#                     "cyan",
#                 ),
#                 end=end,
#                 flush=True,
#             )
#         elif gen == "system":
#             print(
#                 colored(
#                     f"\n{agent_name}: {content}",
#                     "red",
#                 ),
#                 end=end,
#                 flush=True,
#             )
#         elif gen == "tool":
#             print(
#                 colored(
#                     f"\n{agent_name}: {content}",
#                     "blue",
#                 ),
#                 end=end,
#                 flush=True,
#             )
#         elif gen == "search":
#             print(
#                 colored(
#                     f"\nurl: {content}",
#                     "cyan",
#                 ),
#                 end=end,
#                 flush=True,
#             )


def obj_to_dict(obj):
    if isinstance(obj, list):
        return [obj_to_dict(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        result = {}
        for key, val in obj.__dict__.items():
            if key.startswith("_"):
                continue
            element = []
            if isinstance(val, list):
                for item in val:
                    if hasattr(item, "__dict__"):
                        element.append(obj_to_dict(item))
                    else:
                        element.append(item)
            elif hasattr(val, "__dict__"):
                element = obj_to_dict(val)
            else:
                element = val
            result[key] = element
        return result
    else:
        return obj
