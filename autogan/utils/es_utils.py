import json
from asyncio import Queue
from typing import Dict, Optional

from autogan.protocol.response_protocol import ResponseProtocol
from elasticsearch import Elasticsearch

from autogan.utils.vector_utils import VectorTool


def _chat_file_index(dims: int) -> Dict:
    return {
        "mappings": {
            "properties": {
                "user_id": {
                    "type": "keyword"
                },
                "conversation_id": {
                    "type": "keyword"
                },
                "file_name": {
                    "type": "keyword"
                },
                "slice": {
                    "type": "keyword"
                },
                "vector": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine",
                },
                "text": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
            }
        }
    }


def _user_file_index(dims: int) -> Dict:
    return {
        "mappings": {
            "properties": {
                "user_id": {
                    "type": "keyword"
                },
                "base_id": {
                    "type": "keyword"
                },
                "file_name": {
                    "type": "keyword"
                },
                "slice": {
                    "type": "keyword"
                },
                "vector": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine",
                },
                "text": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
            }
        }
    }


def _web_detail_index(dims: int) -> Dict:
    return {
        "mappings": {
            "properties": {
                "keyword": {
                    "type": "keyword"
                },
                "url": {
                    "type": "keyword"
                },
                "title": {
                    "type": "keyword"
                },
                "slice": {
                    "type": "keyword"
                },
                "vector": {
                    "type": "dense_vector",
                    "dims": dims,
                    "index": True,
                    "similarity": "cosine",
                },
                "text": {
                    "type": "text",
                    "analyzer": "ik_max_word"
                },
            }
        }
    }


class ESSearch:
    def __init__(
            self,
            host: str,
            port: int,
            dims: Optional[int] = None
    ):
        self.es = Elasticsearch(f"http://{host}:{port}")
        self.dims = dims if dims else 512
        self.create_index("chat_file_index", _chat_file_index(self.dims))
        self.create_index("user_file_index", _user_file_index(self.dims))
        self.create_index("web_detail_index", _web_detail_index(self.dims))
        self.VectorTool= VectorTool(dims=self.dims)

    def create_index(self, index_name: str, body: Dict):
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name, ignore=400, body=body)

    def add_document(self, index_name: str, doc: Dict):
        self.es.index(index=index_name, document=doc)

    def add_chat_file(self, user_id: int, conversation_id: int, file_name: str, file: str, response: Optional[Queue] = None):
        values = self.VectorTool.text_to_vectors(file, response)
        l = len(values)
        for i, value in enumerate(values):
            data = {
                "step": "add_chat_file",
                "index": i + 1,
                "length": l,
            }
            text = f'data: {json.dumps(data, ensure_ascii=False)}\n\n'
            response.put(text)
            value["user_id"] = user_id
            value["conversation_id"] = conversation_id
            value["file_name"] = file_name
            value["slice"] = i
            self.es.index(index="chat_file_index", document=value)

    def add_user_file(self, user_id: int, base_id: int, file_name: str, file: str, response: Optional[Queue] = None):
        values = self.VectorTool.text_to_vectors(file, response)
        l = len(values)
        for i, value in enumerate(values):
            value["user_id"] = user_id
            value["base_id"] = base_id
            value["file_name"] = file_name
            value["slice"] = i
            self.es.index(index="user_file_index", document=value)
            data = {
                "step": "add_document",
                "index": i+1,
                "length": l,
            }
            text = f'data: {json.dumps(data, ensure_ascii=False)}\n\n'
            response.put(text)

    def _web_detail_index(self, keyword: int, url: int, title: str, detail: str):
        values = self.VectorTool.text_to_vectors(detail)
        for i, value in enumerate(values):
            value["keyword"] = keyword
            value["url"] = url
            value["title"] = title
            value["slice"] = i
            self.es.index(index="web_detail_index", document=value)