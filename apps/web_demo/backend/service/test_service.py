from typing import Optional

from oss2 import Bucket

import autogan

from apps.web_demo.backend.service.service import UniversalService
from autogan.protocol.storage_protocol import StorageProtocol
from autogan.utils.es_utils import ESSearch


class TestService(UniversalService):
    def __init__(
            self,
            default_agent_config: str,
            super_rich: Optional[str] = None,
            stream_mode: Optional[bool] = None,
            storage: Optional[StorageProtocol] = None,
            es: Optional[ESSearch] = None,
            bucket: Optional[Bucket] = None
    ):
        llm_config_dict = autogan.dict_from_json(default_agent_config)
        human = autogan.HumanAgent("Customer", "请帮助我完成业务", autogan.InputModel.API)
        human.pipeline = "\\"
        cust_manager = autogan.UniversalAgent("CustomerManager", "负责接待客户", work_flow="""
1. 你是一个富有经验的客户经理，请尽一切可能满足客户的合法需求，但请注意使用与客户相同的语言进行回复。

2. 如果没有正确答案，请明确告知，而不是给出错误结果

3. 如客户有建议、投诉、合作等要求，请先 @Customer 问清客户的联系方式和具体要求后，再告知 @Secretary。注意：一定要获得对方的联系方式，如未提供可反复询问
""")
        search_config_dict = autogan.dict_from_json("SEARCH_CONFIG")
        search_exp = autogan.ToolAgentSearch(search_config_dict, name="SearchExpert")
        mail_config_dict = autogan.dict_from_json("MAIL_CONFIG")
        secretary = autogan.ToolAgentMail(mail_config_dict, name="Secretary")
        file_exp = autogan.ToolAgentDocument()
        coder = autogan.UniversalAgent("Coder", duty="我可以编写 python 代码并执行，但注意我并不能绘制图片（不能绘制趋势图、饼状图、柱状图等），因此请不要在任务中包括绘图内容。", work_flow="""
1. 我希望你是一个有经验的Python程序员，将接收到的需求用代码来实现。不用管你自己是否有能力执行代码，因为 Tester 可以帮你执行。

2. 你的代码需要先 @Tester，并将代码使用 ``` 符号封装，他会回复执行结果，例如：
@Tester 请帮我执行代码
```python
Your code
print(xxx)
```
注意：你的结果必须以print进行输出，否则无法得到反馈。

3. 当运行结果提示 No module 时，请不要轻易放弃，你可以通过提交指令来安装缺少的 module，例如：
```
pip install xxx
```

4. 如果收到绘图任务（如趋势图、饼状图、柱状图等）请拒绝，不要尝试用 python 代码绘图""")
        test_staff = autogan.ToolAgentCodeExecution("Tester")
        painter_exp = autogan.ToolAgentPainter(bucket)

        org_structure = [human, cust_manager, search_exp, secretary, file_exp, painter_exp, [coder, test_staff]]

        super().__init__(
            llm_config_dict,
            org_structure,
            "hello",
            super_rich,
            stream_mode,
            storage,
            es,
            cust_manager
        )
