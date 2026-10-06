"""
数据准备模块
"""

import logging
import hashlib
from typing import List,Dict
from langchain_core.documents import Document
from pathlib import Path
import json
import re
import uuid
logger=logging.getLogger(__name__)

class DataPreparationModule:
    """数据准备模块 - 负责数据加载、清洗和预处理"""
    CATEGORY_MAPPING = {
        'meat_dish': '荤菜',
        'vegetable_dish': '素菜',
        'soup': '汤品',
        'dessert': '甜品',
        'breakfast': '早餐',
        'staple': '主食',
        'aquatic': '水产',
        'condiment': '调料',
        'drink': '饮品'
    }
    CATEGORY_TABELS=list(set(CATEGORY_MAPPING.values()))
    DIFFICULTY_TABELS=['非常简单', '简单', '中等', '困难', '非常困难']

    def __init__(self,data_path:str):
        """
        初始化数据准备模块
        
        Args:
            data_path: 数据文件夹路径
        """
        self.data_path=data_path
        self.documents:List[Document]=[]  #父文档
        self.chunks:List[Document]=[]  #子文档
        self.parent_child_map:Dict[str,str]={}  #子块ID->父文档ID的映射

    def load_documents(self)->List[Document]:
        """
        加载文档数据
        
        Returns:
            加载的文档列表
        """
        logger.info(f"正在从 {self.data_path} 加载文档...")

        documents=[]
        data_path_obj=Path(self.data_path)
        # print(f"self.data_path:{self.data_path}")
        # print(f"Path(self.data_path):{Path(self.data_path)}")
        count=0
        for md_file in data_path_obj.rglob("*.md"):
            if count==1:
                break
            count+=1
           
            try:
                print(f"md_file:{md_file}")
                print("="*60)
                with open(md_file,'r',encoding='utf-8') as f:
                    content=f.read()
             
                
                #为每个父文档分配确定性的唯一ID（基于数据根目录的相对路径）
                try:
                    data_root=Path(self.data_path).resolve()
                    # print(f"data_root:{data_root}")
                    relative_path=Path(md_file).resolve().relative_to(self.data_path).as_posix()
                    # print(f"relative_path:{relative_path}")
                except Exception:
                    relative_path=Path(md_file).as_posix()
                parent_id=hashlib.md5(relative_path.encode("utf-8")).hexdigest()
                # print(f"parent_id:{parent_id}")
                doc = Document(
                    page_content=content,
                    metadata={
                        "source": str(md_file),
                        "parent_id": parent_id,
                        "doc_type": "parent"  # 标记为父文档
                    }
                )
                documents.append(doc)

            except Exception as e:
                logger.warning(f"读取文件{md_file}失败:{e}")
        return documents
    def _enhance_metadata(self,doc:Document):
        """
            增强文档元数据
            
            Args:
                doc: 需要增强元数据的文档
        """
        file_path = Path(doc.metadata.get('source', ''))
        path_parts = file_path.parts
        
        # 提取菜品分类
        doc.metadata['category'] = '其他'
        for key, value in self.CATEGORY_MAPPING.items():
            if key in path_parts:
                doc.metadata['category'] = value
                break
        
        # 提取菜品名称
        doc.metadata['dish_name'] = file_path.stem

        # 分析难度等级（使用正则精确匹配连续星号数量）
        content = doc.page_content
        star_match = re.search(r'★+', content)
        if star_match:
            star_count = len(star_match.group())
            difficulty_map = {5: '非常困难', 4: '困难', 3: '中等', 2: '简单', 1: '非常简单'}
            doc.metadata['difficulty'] = difficulty_map.get(star_count, '未知')
        else:
            doc.metadata['difficulty'] = '未知' 

test=DataPreparationModule(data_path="C:/Users/33052/Desktop/all-in-rag/data/C8/cook")

d=test.load_documents()
parts=test._enhance_metadata(d[0])

from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
            ("#", "主标题"),      # 菜品名称
            ("##", "二级标题"),   # 必备原料、计算、操作等
            ("###", "三级标题")   # 简易版本、复杂版本等
        ]


markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=False  # 保留标题，便于理解上下文
        )
markdown_splitter1 = MarkdownHeaderTextSplitter(
            headers_to_split_on=headers_to_split_on,
            strip_headers=True  # 保留标题，便于理解上下文
        )
md_chunks = markdown_splitter.split_text(d[0].page_content)
md_chunks1 = markdown_splitter1.split_text(d[0].page_content)

parent_id = d[0].metadata["parent_id"]

# print(md_chunks)
# print("="*60)
# print(md_chunks1)

print(f"父块的元数据：\n{json.dumps(d[0].metadata,indent=4,ensure_ascii=False)}")
print("="*60)

print(f"合并前  第一块子块的元数据：\n{json.dumps(md_chunks[0].metadata,indent=4,ensure_ascii=False)}")
print("="*60)

for i, chunk in enumerate(md_chunks):
                    # 为子块分配唯一ID
                    child_id = str(uuid.uuid4())

                    # 合并原文档元数据和新的标题元数据
                    chunk.metadata.update(d[0].metadata)
                    chunk.metadata.update({
                        "chunk_id": child_id,
                        # "parent_id": parent_id, #可以删掉，合并父块metadata时就已经添加了
                        "doc_type": "child",  # 标记为子文档
                        "chunk_index": i      # 在父文档中的位置
                    })


print(f"合并后  第一块子块的元数据：\n{json.dumps(md_chunks[0].metadata,indent=4,ensure_ascii=False)}")
print("="*60)


