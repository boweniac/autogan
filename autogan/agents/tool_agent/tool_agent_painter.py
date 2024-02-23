import re
from collections import defaultdict
from typing import Optional, Dict, List

from oss2 import Bucket

from autogan.oai.image_api_utils import ImageRequest
from autogan.oai.image_generate_utils import generate_image
from autogan.tools.code_execution_tool import CodeExecution

from autogan.tools.wolfram_alpha_tool import WolframAlphaAPIWrapper

from autogan.oai.count_tokens_utils import count_text_tokens

from autogan.agents.universal_agent import UniversalAgent
from autogan.utils.compressed_text_utils import compressed_text_universal
from autogan.tools.web_search_tool import WebSearch


class ToolAgentPainter(UniversalAgent):
    def __init__(
            self,
            bucket: Bucket,
            agent_llm_config: Optional[Dict] = None,
            name: Optional[str] = "PainterExp",
            duty: Optional[str] | Optional[dict] = None,
            work_flow: Optional[str] | Optional[dict] = None,
            work_dir: Optional[str] = "extensions",
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
            "EN": """I am a picture generation assistant, capable of producing images using.""",
            "CN": """我是一个图片生成助手，可以利用 matplotlib 或是 stable diffusion 模型来生成图片"""
        }
        work_flow = work_flow if work_flow else {
            "EN": """I hope you are an expert in image generation. You have the following two tools to choose from:

1. python: You can generate images by writing code, note that you can only generate one image at a time, and please output the image file name with the print function at the end of the code.
When using, please output the code and add the python symbol on the outside, for example:
```python
import matplotlib.pyplot as plt

years = ['2012', '2013', '2014']
values = [13, 15, 18]

plt.figure(figsize=(10, 6))
plt.plot(years, values, marker='o')
plt.title('Yearly Values')
plt.xlabel('Year')
plt.ylabel('Value')
plt.grid(True)
plt.savefig('line_chart.png')
print('line_chart.png')
```

2. model: You can call the stable diffusion model to generate images.
When using, please output the image prompt and add the model symbol on the outside, for example:
```model
xx style, xx content
```

Note: When you decide to use a tool, please do not @ anyone.""",
            "CN": """我希望你是一个图片生成专家。您有以下两个工具可供选择:
1. python:你可以通过编写代码来生成图片，注意每次只能生成一张图片，并且在代码的最后请以 print 函数输出图片文件名。
使用时，请在输出代码并在外层加上 python 符号，例如:

```python
import matplotlib.pyplot as plt

years = ['2012', '2013', '2014']
values = [13, 15, 18]

plt.figure(figsize=(10, 6))
plt.plot(years, values, marker='o')
plt.title('Yearly Values')
plt.xlabel('Year')
plt.ylabel('Value')
plt.grid(True)
plt.savefig('line_chart.png')
print('line_chart.png')
```

2. model:您可以调用 stable diffusion 模型来生成图片。
使用时，请在输出图片提示词并在外层加上 model 符号，例如:
```model
xx 风格，xx 内容
```

注意:当您决定使用某个工具时，请不要@任何人。
"""
        }
        super().__init__(
            name,
            agent_llm_config=agent_llm_config,
            duty=duty,
            work_flow=work_flow,
            agent_type="TOOLMAN"
        )
        self._code_execution = CodeExecution(work_dir)
        self._bucket = bucket

    def tool_parameter_identification(self, content: Optional[str] = None) -> tuple[List[tuple], str, str]:
        param_list = CodeExecution.extract_code(content)
        return param_list, "Generating", "Generate results"

    def tool_call_function(self, conversation_id: int, task_id: int, tool: str, param: str | dict) -> tuple[str, int]:
        if tool == "python" and param:
            content, completion_tokens = self._matplotlib_function(conversation_id, param)
            return content, completion_tokens
        elif tool == "model" and param:
            content, completion_tokens = self._model_function(param)
            return content, completion_tokens
        else:
            return """Please make a choice between web and wolfram, and use the ``` symbol for encapsulation, for example:
```wolfram
one wolfram query
```""", 18

    def _matplotlib_function(self, conversation_id: int, param: str) -> tuple[str, int]:
        print(f"param: {param}")
        try:
            execution_result, tokens, output = self._code_execution.code_execution_reply(param)
            if output:
                output = output.rstrip("\n")
                self._bucket.put_object_from_file(f"{conversation_id}/{output}", f"extensions/{output}")
                return f'![Example Image](https://aibowen-base.boweniac.top/{conversation_id}/{output})', tokens
            else:
                raise ValueError("Code execution failed.")
        except Exception as e:
            print(e)
            return ("Code execution failed, please make sure that the code guard has added ``` symbols at the， To "
                    "install dependencies, use the python3 -m pip install xxx statement"
                    "beginning and end"), 20

    @staticmethod
    def _model_function(param: str) -> tuple[str, int]:
        image_request = ImageRequest(param)
        image = generate_image(image_request)
        if image:
            return f'![Example Image]({image})', 1
        else:
            return "Request failed, you can choose to retry", 8
