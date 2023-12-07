import os
import pathlib
import re
import signal
import subprocess
import sys
from hashlib import md5
from typing import Tuple, Optional
from autogan.oai.count_tokens_utils import count_text_tokens

try:
    from termcolor import colored
except ImportError:
    def colored(x, *args, **kwargs):
        return x


class CodeExecution:
    def __init__(self, work_dir: Optional[str] = None):
        """A class for code execution
        用于代码执行的类

        Supports python, bash, shell, powershell code
        支持 python, bash, shell, powershell 代码

        Please note when using:
        使用时请注意：

        1.Code must be encapsulated with ``` symbol
        1.代码必须使用 ``` 符号封装

        2.Must be run in a docker environment
        2.须在 docker 环境中运行

        :param work_dir: The relative path for code execution, default is extensions
            执行代码的相对路径，默认为 extensions
        """
        if work_dir is None:
            work_dir = "extensions"
        self._work_dir = os.getcwd() + "/" + work_dir
        self._win32 = sys.platform == "win32"
        self._path_separator = self._win32 and "\\" or "/"

    def code_execution_reply(self, text: str) -> Tuple[str, int]:
        """Execute code and return result
        执行代码并返回结果

        :param text: Code must be encapsulated with ``` symbol
            代码必须使用 ``` 符号封装

        :return:
            --execution_result: Execution result
                执行结果
            --tokens: Tokens of the execution result
                执行结果的 tokens
        """

        # Determine whether it is running in docker
        if os.path.exists("/.dockerenv"):
            lang, code = self.extract_code(text)
            if code is None:
                exitcode = 1
                output = "Submit your Python code to me and I can tell you the execution result. But I can't write code or talk to you. So please just submit the completed code to me encapsulated with ``` symbols. And you should always use the 'print' function for the output"
            else:
                exitcode, output = self.execute(code, lang=lang)
        else:
            exitcode = 1
            output = "executing code needs to run in a docker environment"

        if not output:
            exitcode = 1
            output = "You should always use the 'print' function for the output"

        result = "execution succeeded" if exitcode == 0 else "execution failed"
        if exitcode != 0:
            output += "\nIf you need to install dependencies, you can send me the code for installing dependencies. Like ```pip install openai```"
            execution_result = f"exitcode: {exitcode} ({result})\n{output}"
        else:
            execution_result = f"exitcode: {exitcode} ({result})\nCode output: \n{output}"
        tokens = count_text_tokens(execution_result)

        return execution_result, tokens

    def execute(
            self,
            code: str,
            lang: Optional[str] = None,
            timeout: Optional[int] = 600,
    ) -> Tuple[int, str]:
        """Execute code
            执行代码

        :param code: Code to be executed
        :param lang: Code language, if empty, will try to infer the language from the code
        :param timeout: Maximum code execution time (seconds)

        :return:
            --exitcode: exitcode
            --output: Execution result
        """
        try:
            if not lang:
                lang = self.infer_lang(code)

            if lang not in ["bash", "shell", "sh", "python", "Python"]:
                return 1, "unknown language"

            print(
                colored(
                    f"\n\n>>>>>>>> EXECUTING CODE BLOCK (language is {lang})...",
                    "red",
                ),
                flush=True,
            )

            if self._win32 and lang in ["sh", "shell"]:
                lang = "ps1"

            # Create a temporary file
            code_hash = md5(code.encode()).hexdigest()
            filename = f"tmp_code_{code_hash}.{'py' if lang.startswith('python') else lang}"
            filepath = os.path.join(self._work_dir, filename)
            file_dir = os.path.dirname(filepath)
            os.makedirs(file_dir, exist_ok=True)

            # Write the code into a temporary file
            with open(filepath, "w", encoding="utf-8") as tmp_code:
                tmp_code.write(code)

            # Execute code
            cmd = [
                sys.executable if lang.startswith("python") or lang.startswith("Python") else self._cmd(lang),
                f".\\{filename}" if self._win32 else filename,
            ]
            if self._win32:
                result = subprocess.run(
                    cmd,
                    cwd=self._work_dir,
                    capture_output=True,
                    text=True,
                )
            else:
                signal.signal(signal.SIGALRM, self._timeout_handler)
                try:
                    signal.alarm(timeout)
                    # run the code in a subprocess in the current docker container in the working directory
                    result = subprocess.run(
                        cmd,
                        cwd=self._work_dir,
                        capture_output=True,
                        text=True,
                    )
                    signal.alarm(0)
                except TimeoutError:
                    os.remove(filepath)
                    return 1, "Timeout"

            os.remove(filepath)
            if result.returncode:
                logs = result.stderr
                abs_path = str(pathlib.Path(filepath).absolute())
                logs = logs.replace(str(abs_path), "").replace(filename, "")
            else:
                logs = result.stdout

            return result.returncode, logs
        except Exception as e:
            return 1, f"execution error: {e}"

    @staticmethod
    def extract_code(text: str) -> Tuple[Optional[str], Optional[str]]:
        """Extract code from text

        :param text: 包含代码的文本，代码必须以```符号封装

        :return:
            --lang: Code must be encapsulated with ``` symbol
            --code: Code to be executed
        """
        match = re.findall(r"```(\w*)\n(.*?)\n```", text, flags=re.DOTALL)
        return match[0] if match else (None, None)

    @staticmethod
    def infer_lang(code) -> str:
        """Infer code language

        :param code: Code to be executed

        :return: The inferred code language, if the inference fails, it will return unknown
        """
        if (code.startswith("python ") or code.startswith("pip") or code.startswith("python3 ")
                or code.startswith("pip3")):
            return "sh"

        try:
            compile(code, "test", "exec")
            return "python"
        except SyntaxError:
            return "unknown"

    @staticmethod
    def _timeout_handler(signum, frame):
        raise TimeoutError("Timed out!")

    @staticmethod
    def _cmd(lang):
        if lang.startswith("python") or lang in ["bash", "sh", "powershell"]:
            return lang
        if lang in ["shell"]:
            return "sh"
        if lang in ["ps1"]:
            return "powershell"
        raise NotImplementedError(f"{lang} not recognized in code execution")
