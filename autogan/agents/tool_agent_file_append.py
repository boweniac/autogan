from typing import Optional
from autogan.agents.universal_agent import UniversalAgent
from autogan.oai.count_tokens_utils import count_text_tokens
from autogan.tools.file_tool import File
from autogan.utils.json_utils import text_to_json


class ToolAgentFileAppend(UniversalAgent):
    def __init__(
            self,
            name: Optional[str] = "FileAppendSpec",
            duty: Optional[str] = 'I can append the text content sent to me to the end of a specified docx document. \n'
                                  'Please note that I only accept a fixed json format: \n'
                                  '{"file_name": "File name without extension", "text": "Text to be appended"}.',
            # duty: Optional[str] = '我可以将发送给我的文本内容追加到指定 docx 文档的结尾，'
            #                       '注意我只接收固定的json格式：'
            #                       '{"file_name": "不带扩展名的文件名称", "text": "待追加的文本内容"}',
            work_dir: Optional[str] = None,
    ):
        """FileAppendSpecialist

        Append text to the end of the word file

        Receive a JSON string, fields include:
            - file_name：File name without extension
            - text：Text content to be appended

        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        :param work_dir: The relative path of the document, default is extensions
        """
        super().__init__(
            name,
            duty=duty,
            use_tool="only"
        )
        self._file = File(work_dir)

    def tool_function(self, task_id: str, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        param = text_to_json(param)
        if param:
            reply = self._file.append_to_word(param['file_name'], param['text'])

            if reply:
                param = f"Text appended successfully, saved to: {param['file_name']}.docx"
                tokens = count_text_tokens(param)
                return param, tokens

        return ('Failed to append the text, please ensure the text to be appended is sent in the '
                'format of {"file_name": "file name without extension", "text": "text to be '
                'appended"}.'), 39
