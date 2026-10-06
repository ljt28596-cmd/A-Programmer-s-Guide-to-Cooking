from index_construction import IndexConstructionModule
import json
from data_preparation import DataPreparationModule

path="C:/Users/33052/Desktop/all-in-rag/data/C8/cook"
module=DataPreparationModule(data_path=path)

doc=module.load_documents()


aquatic=module.filter_documents_by_category(category="水产")
drink=module.filter_documents_by_category(category="饮品")



chunks_aquatic=module.my_chunk_documents(docs=aquatic)
chunks_drink=module.my_chunk_documents(docs=drink)


index=IndexConstructionModule()



index.build_vector_index(chunks_aquatic)

index.save_index()

print("="*60)
search=index.similarity_search(query="虾",k=2)
docs_as_dict = [
    {"page_content": d.page_content, "metadata": d.metadata}
    for d in search
]
print(json.dumps(docs_as_dict, ensure_ascii=False, indent=4, default=str))

print("="*60)
search=index.similarity_search(query="柠檬水",k=2)
docs_as_dict = [
    {"page_content": d.page_content, "metadata": d.metadata}
    for d in search
]
print(json.dumps(docs_as_dict, ensure_ascii=False, indent=4, default=str))

index.add_documents(chunks_drink)

index.save_index()

print("="*60)
search=index.similarity_search(query="虾",k=2)
docs_as_dict = [
    {"page_content": d.page_content, "metadata": d.metadata}
    for d in search
]
print(json.dumps(docs_as_dict, ensure_ascii=False, indent=4, default=str))

print("="*60)
search=index.similarity_search(query="柠檬水",k=2)
docs_as_dict = [
    {"page_content": d.page_content, "metadata": d.metadata}
    for d in search
]
print(json.dumps(docs_as_dict, ensure_ascii=False, indent=4, default=str))


#测试数据库覆盖问题，先load、save chunks_aquatic然后add、save chunks_drink
#my_chunk_documents和_my_markdown_header_split可能会有bug
#测试similarity_search
#测试load