from dataclasses import dataclass,asdict
import json
from typing import Dict,Any

@dataclass
class RAGConfig:
    """RAG系统配置类"""
    data_path:str="../../data/C8/cook"
    index_save_path:str="./vector_index"

    embedding_model:str="BAAI/bge-small-zh-v1.5"
    llm_model:str="qwen3.7-flash"

    top_k:int=3

    temperature:float=0.1
    max_token:int=2048

    @classmethod
    def from_dict(cls,config_dict:Dict[str,Any])->'RAGConfig':
        """从字典创建配置对象"""
        return cls(**config_dict)

    def to_dict(self)->Dict[str,Any]:
        """转换为字典"""
        return asdict(self)

DEFAULT_CONFIG=RAGConfig()