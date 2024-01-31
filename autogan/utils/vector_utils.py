import json
from asyncio import Queue
from typing import Optional

from autogan.protocol.response_protocol import ResponseProtocol
from transformers import AutoTokenizer, AutoModel
import torch


class VectorTool:
    def __init__(
            self,
            model_name: Optional[str] = None,
            dims: Optional[int] = None,
    ):
        self.dims = dims if dims else 512
        self.model_name = model_name if model_name else "bert-base-uncased"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)

    def split_text(self, text: str):
        segments = []
        segment = ""
        b = 0

        for char in text:
            char_bytes = len(char.encode('utf-8'))
            if b + char_bytes > self.dims:
                segments.append(segment)
                segment = char
                b = char_bytes
            else:
                segment += char
                b += char_bytes

        # 添加最后一个片段
        if segment:
            segments.append(segment)

        return segments

    def text_to_vector(self, text: str):
        input_ids = self.tokenizer.encode(text, add_special_tokens=True)
        input_ids = torch.tensor([input_ids])
        with torch.no_grad():
            outputs = self.model(input_ids)
            hidden_states = outputs[0]
        vector = hidden_states.squeeze(0)[-1]
        return vector

    def text_to_vectors(self, text, response: Optional[Queue] = None):
        # 拆分文本成多个片段
        text_segments = self.split_text(text)
        values = []
        # for segment in text_segments:
        length = len(text_segments)
        for i, segment in enumerate(text_segments):
            vector = self.text_to_vector(segment)
            value = {
                "vector": vector.numpy().tolist(),
                "text": segment
            }
            values.append(value)
            data = {
                "step": "text_to_vectors",
                "index": i+1,
                "length": length,
            }
            text = f'data: {json.dumps(data, ensure_ascii=False)}\n\n'
            response.put(text)
        return values
