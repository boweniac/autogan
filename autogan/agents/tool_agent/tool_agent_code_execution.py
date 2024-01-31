from typing import Optional
from autogan.agents.universal_agent import UniversalAgent, AgentType
from autogan.tools.code_execution_tool import CodeExecution


class ToolAgentCodeExecution(UniversalAgent):
    def __init__(
            self,
            name: Optional[str] = "CodeExecSpec",
            duty: Optional[str] = "Submit your Python code to me and I can tell you the execution result. But I can't write code or talk to you. So please just submit the completed code to me encapsulated with ``` symbols. And you should always use the 'print' function for the output",
            # duty: Optional[str] = "我不会写代码，但可以执行你提交给我的代码，并返回执行结果。",
            work_dir: Optional[str] = "extensions"
    ):
        """CodeExecutionSpecialist

        Execute code and return results

        Supports python, bash, shell, powershell code

        Please note when using:

        1.Code must be encapsulated with ``` symbol

        2.Must be run in a docker environment

        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        :param work_dir: The relative path of the executing code, default is extensions
        """
        super().__init__(
            name,
            duty=duty,
            agent_type="TOOL"
        )
        self._code_execution = CodeExecution(work_dir)

    def tool_function(self, task_id: int, lang: Optional[str] = None, code: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        try:
            execution_result, tokens = self._code_execution.code_execution_reply(code)
            if execution_result:
                return execution_result, tokens
            else:
                raise ValueError("Code execution failed.")
        except Exception as e:
            print(e)
            return ("Code execution failed, please make sure that the code guard has added ``` symbols at the， To "
                    "install dependencies, use the python3 -m pip install xxx statement"
                    "beginning and end"), 20
