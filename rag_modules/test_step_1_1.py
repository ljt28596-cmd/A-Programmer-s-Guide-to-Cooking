from index_construction import IndexConstructionModule
import json
from data_preparation import DataPreparationModule

path="C:/Users/33052/Desktop/all-in-rag/data/C8/cook"
module=DataPreparationModule(data_path=path)


index=IndexConstructionModule()

index.load_index()

search_xia=index.similarity_search(query="虾",k=2)

docs_as_dict = [
    {"page_content": d.page_content, "metadata": d.metadata}
    for d in search_xia
]

print(json.dumps(docs_as_dict, ensure_ascii=False, indent=4, default=str))