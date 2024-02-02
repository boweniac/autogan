import json
from asyncio import Queue
from typing import Dict, Optional

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
        self.VectorTool = VectorTool(dims=self.dims)

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

    def get_chat_file_pack(self, conversation_id: int, file_name: str, pack_size: int):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"conversation_id": conversation_id}},
                        {"match": {"file_name": file_name}}
                    ]
                }
            },
            "sort": [
                {"slice": {"order": "asc"}}  # 按slice字段升序排序
            ]
        }
        response = self.es.search(index="chat_file_index", body=query)
        print(f"response: {response}")
        values = []
        i = 1
        text = ""
        for value in response["hits"]["hits"]:
            text += value["_source"]["text"]
            values.append(text)
            if i == pack_size:
                i = 1
                text = ""
            else:
                i += 1
        return values

    def get_chat_file_hybrid(self, conversation_id: int, file_name: str, keyword: str):
        vectors = self.VectorTool.text_to_vectors(keyword)
        query = {
            "size": 10,
            "query": {
                "bool": {
                    "must": [
                        {"match": {"conversation_id": conversation_id}},
                        {"match": {"file_name": file_name}},
                        {"match": {"text": keyword}}
                    ],
                    "should": [
                        {"script_score": {
                            "query": {"match_all": {}},
                            "script": {
                                "source": "cosineSimilarity(params.query_vector, 'vector') + 1.0",
                                "params": {"query_vector": vectors[0]["vector"]}
                            }
                        }}
                    ]
                }
            }
        }
        response = self.es.search(index="chat_file_index", body=query)
        values = []
        for value in response["hits"]["hits"]:
            text = self.get_chat_file_slice(conversation_id, file_name, value["_source"]["slice"], value["_source"]["text"])
            values.append(text)
        return values

    def get_chat_file_slice(self, conversation_id: int, file_name: str, slice: int, text: str):
        slice_text = ""
        if slice > 0:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"term": {"conversation_id": conversation_id}},
                            {"term": {"file_name": file_name}},
                            {"term": {"slice": slice-1}}
                        ]
                    }
                }
            }
            response = self.es.search(index="chat_file_index", body=query)
            slice_text = response["hits"]["hits"][0]["_source"]["text"]
        slice_text += text
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"term": {"conversation_id": conversation_id}},
                        {"term": {"file_name": file_name}},
                        {"term": {"slice": slice - 1}}
                    ]
                }
            }
        }
        response = self.es.search(index="chat_file_index", body=query)
        if response["hits"]["hits"]:
            slice_text = response["hits"]["hits"][0]["_source"]["text"]
        return slice_text