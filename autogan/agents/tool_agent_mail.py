from typing import Optional, Dict
from autogan.agents.universal_agent import UniversalAgent
from autogan.utils.json_utils import text_to_json
from autogan.tools.mail_tool import SendEmail


class ToolAgentMail(UniversalAgent):
    def __init__(
            self,
            email_config: Dict,
            name: Optional[str] = "MailSpec",
            duty: Optional[str] = 'I can assist you in sending emails, '
                                  'but please note that I only accept a specific JSON format: \n'
                                  '{"to": ["Recipient Email 1", "Recipient Email 2"], "subject": "Email Subject", '
                                  '"text": "Email Body", "files": ["Attachment Name 1", "Attachment Name 2"]}. \n'
                                  'The "files" field is optional.',
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
        super().__init__(
            name,
            duty=duty,
            use_tool="only"
        )
        self._send_email = SendEmail(email_config, work_dir)

    def tool_function(self, task_id: str, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        try:
            param = text_to_json(param)
            if param:
                reply = self._send_email.send(param['to'], param['subject'], param['text'], param['files'])

                if reply:
                    return "Mail sending success", 3

            raise ValueError("Mail sending failure.")
        except Exception as e:
            print(e)
            return ('I can help you send emails, but please note that I only accept a fixed json format: {"to": ['
                    '"Recipient Email 1", "Recipient Email 2"], "subject": "Email Subject", "text": "Email Body", '
                    '"files": ["Attachment 1", "Attachment 2"]}.'), 62
