import sys
from typing import Optional
from autogan.agents.universal_agent import UniversalAgent
from autogan.oai.count_tokens_utils import count_text_tokens


class HumanAgent(UniversalAgent):
    def __init__(
            self,
            name,
            duty: Optional[str] = None,
    ):
        """Human agent

        Interact with other agents through forms.

        :param name: The agent name should be unique in the organizational structure.
        :param duty: Used to explain one's job responsibilities to other agents.
        """
        super().__init__(
            name,
            duty=duty,
            use_tool="only"
        )

    def tool_function(self, task_id: str, param: Optional[str] = None,
                      tokens: Optional[int] = None) -> tuple[str, int]:
        try:
            reply = input("Please enter: ")
            if reply:
                tokens = count_text_tokens(reply)
                return reply, tokens
            else:
                sys.exit()
        except KeyboardInterrupt:
            sys.exit()
        except Exception as e:
            sys.exit()
