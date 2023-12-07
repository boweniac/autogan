import tiktoken
from typing import Optional


def count_text_tokens(text: str, model: Optional[str] = "gpt-3.5-turbo") -> int:
    """Calculate the tokens of the text.

    :param text: The text to be tokenized
    :param model: Calculate tokens for a specific model. If the model is not listed, it will default to calculating the number of tokens based on the gpt-3.5-turbo standard.

    :return: tokens
    """

    if not text:
        return 0

    model_list = ['gpt-4', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo']
    if model not in model_list:
        model = "gpt-3.5-turbo"

    try:
        encoding = tiktoken.encoding_for_model(model)
        num_tokens = len(encoding.encode(text))
    except Exception as e:
        print(e)
        num_tokens = 0

    return num_tokens
