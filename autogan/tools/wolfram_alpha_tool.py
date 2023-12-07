import wolframalpha
from time import sleep
from typing import Dict, Optional


class WolframAlphaAPIWrapper:
    def __init__(self, wolfram_config: Dict):
        """Wrapper for Wolfram Alpha.

        :param wolfram_config: JSON format of email_config
            {"app_id": ""}
        """
        self._wolfram_client = wolframalpha.Client(wolfram_config['app_id'])

    def run(self, query: str) -> Optional[str]:
        from urllib.error import HTTPError

        res = None
        for _ in range(20):
            try:
                res = self._wolfram_client.query(query)
                break
            except HTTPError:
                sleep(1)
            except Exception:
                return None
        if res is None:
            return None

        try:
            if not res["@success"]:
                return None
            assumption = next(res.pods).text
            answer = ""
            for result in res["pod"]:
                if result["@title"] == "Solution":
                    answer = result["subpod"]["plaintext"]
                if result["@title"] == "Results" or result["@title"] == "Solutions":
                    for i, sub in enumerate(result["subpod"]):
                        answer += f"ans {i}: " + sub["plaintext"] + "\n"
                    break
            if answer == "":
                answer = next(res.results).text

        except Exception:
            return None

        if answer is None or answer == "":
            return None

        return f"Assumption: {assumption} \nAnswer: {answer}"
