"""
{'total_documents': 323, 
'total_chunks': 1764, 
'categories': {'水产': 24, 
'早餐': 22, 
'调料': 9, 
'饮品': 21, 
'荤菜': 97, 
'半成品': 10, 
'汤品': 21, 
'主食': 47, 
'素菜': 54, 
'甜品': 17, 
'实例菜': 1}, 
'difficulties': 
{'困难': 78, '中等': 115, '非常简单': 27, '简单': 83, '非常困难': 20}, 
'avg_chunk_size': 129.16496598639455}
"""
import json
from data_preparation import DataPreparationModule

path="C:/Users/33052/Desktop/all-in-rag/data/C8/cook"
module=DataPreparationModule(data_path=path)

doc=module.load_documents()

chunks=module.chunk_documents()

filter_sc=module.filter_documents_by_category(category="水产")
filter_fckn=module.filter_documents_by_difficulty(difficulty="非常困难")

# module.export_metadata(output_path="./metadata.json")