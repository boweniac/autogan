from typing import Optional, Dict, List

from autogan.tools.code_execution_tool import CodeExecution

from autogan.agents.universal_agent import UniversalAgent
from autogan.utils.json_utils import text_to_json
from autogan.tools.mail_tool import SendEmail


class ToolAgentMail(UniversalAgent):
    def __init__(
            self,
            email_config: Dict,
            agent_llm_config: Optional[Dict] = None,
            name: Optional[str] = "MailSpec",
            duty: Optional[str] | Optional[dict] = None,
            work_flow: Optional[str] | Optional[dict] = None,
            # duty: Optional[str] = 'I can assist you in sending emails, '
            #                       'but please note that I only accept a specific JSON format: \n'
            #                       '{"to": ["Recipient Email 1", "Recipient Email 2"], "subject": "Email Subject", '
            #                       '"text": "Email Body", "files": ["Attachment Name 1", "Attachment Name 2"]}. \n'
            #                       'The "files" field is optional.',
            # duty: Optional[str] = '我可以帮你发送邮件，'
            #                       '注意我只接收固定的json格式：'
            #                       '{"to": ["接收邮箱1", "接收邮箱2"], "subject": "邮件标题", '
            #                       '"text": "邮件正文", "files": ["附件名1", "附件名2"]}，其中files字段是可选参数',
            work_dir: Optional[str] = None,
    ):
        """MailSpecialist

        Receive a JSON string, fields include:
            --to：Inbox list
            --subject：Email subject
            --text：Email content
            --files：Attachment name list

        :param email_config: JSON format of email_config
            {"server": "smtp.xxx.xxx", "port": 465, "username": "", "password": ""}
        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        :param work_dir: Attachment relative path, default is extensions
        """
        duty = duty if duty else {
            "EN": """I can assist you in sending external emails, or forwarding feedback and collaboration requests to the company's business department. If you need to send a local file as an attachment, please provide me with the complete filename (including the extension).""",
            "CN": """我可以帮你发送外部邮件，或是将反馈意见与合作需求发送给公司业务部门（但需要你先问清客户的联系方式和具体需求再告知我）。如果需要将本地文件作为附件发送，请告诉我完整的文件名（包括扩展名）"""
        }
        work_flow = work_flow if work_flow else {
            "EN": """When you receive a request to send an email, please convert the request into JSON format and add a mail symbol, for example:
```mail
{"to": ["Recipient Email 1", "Recipient Email 2"], "subject": "Email Subject", "text": "Email Body", "files": ["LocalFile.txt", "LocalFile.pdf"]}.
```
The "files" field is optional.""",
            "CN": """我希望你是公司的秘书，当你收到发送邮件的请求时，请将请求转换为JSON格式输出，并加啥 mail 符号，例如:
```mail
{"to": ["收件人 email 1", "收件人 email  2"], "subject": "主题", "text": "内容主体", "files": ["LocalFile.txt", "LocalFile.pdf"]}.
```

注意：
- 发送建议、投诉、合作意向等需要向公司内部反馈的邮件时，收件人固定为：boweniac@icloud.com
- 其中“files”字段是可选的。"""
        }
        super().__init__(
            name,
            agent_llm_config=agent_llm_config,
            duty=duty,
            work_flow=work_flow,
            agent_type="TOOLMAN"
        )
        self._send_email = SendEmail(email_config, work_dir)

    def tool_parameter_identification(self, content: Optional[str] = None) -> tuple[List[tuple], str, str]:
        param_list = CodeExecution.extract_code(content)
        return param_list, "Sending", "Sent successfully"

    def tool_call_function(self, conversation_id: int, task_id: int, tool: str, param: str | dict) -> tuple[str, int]:
        try:
            param = text_to_json(param)
            if param:
                reply = self._send_email.send(param['to'], param.get("subject", ""), param.get("text", ""), param.get("files", []))

                if reply:
                    return "Mail sending success", 3

            raise ValueError("Mail sending failure.")
        except Exception as e:
            print(e)
            return ('I can help you send emails, but please note that I only accept a fixed json format: {"to": ['
                    '"Recipient Email 1", "Recipient Email 2"], "subject": "Email Subject", "text": "Email Body", '
                    '"files": ["Attachment 1", "Attachment 2"]}.'), 62
