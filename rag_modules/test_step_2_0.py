from data_preparation import DataPreparationModule
from index_construction import IndexConstructionModule
from retrieval_optimization import RetrievalOptimizationModule
import json

path="C:/Users/33052/Desktop/all-in-rag/data/C8/cook"

data=DataPreparationModule(data_path=path)

docuemnts=data.load_documents()

chunks=data.chunk_documents()

index=IndexConstructionModule()

index.build_vector_index(chunks=chunks)

# index.save_index()

retrieve=RetrievalOptimizationModule(
    vectorstore=index.vectorstore,
    chunks=chunks
    )


result=retrieve.hybrid_search(query="蛋")

docs_as_dict = [
    {"page_content": d.page_content, "metadata": d.metadata}
    for d in result
]

print(json.dumps(docs_as_dict, ensure_ascii=False, indent=4, default=str))

print("="*60)
print()
res=retrieve.metadata_filtered_search(
    query="水煮蛋",
    filters={
        'difficulty':["困难","非常困难"],
        'category':'早餐'
    },
    top_k=3
)
docs_as_dict = [
    {"page_content": d.page_content, "metadata": d.metadata}
    for d in res
]

print(json.dumps(docs_as_dict, ensure_ascii=False, indent=4, default=str))
