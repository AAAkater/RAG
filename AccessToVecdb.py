import os

import sys
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter, MarkdownTextSplitter

vecdb_directory: str = os.path.join(os.path.dirname(
    os.path.abspath(sys.argv[0])), 'vecdb')
# 连接数据库
vectordb = Chroma(
    persist_directory=vecdb_directory,
    embedding_function=OpenAIEmbeddings()
)

print(vectordb._collection.count())

# 语义化搜索
question = "some girls"
print(f"{question=}")
docs = vectordb.max_marginal_relevance_search(question, k=3)
for doc in docs:
    print(doc.page_content)


# # 访问本地的Chroma
# persistent_client = chromadb.PersistentClient(path=vecdb_directory)

# # 查看已有集合
# print(persistent_client.list_collections())

# # 选择langchain
# collection_name = 'langchain'
# # 删表
# # persistent_client.delete_collection(collection_name)

# collection = persistent_client.get_or_create_collection(collection_name)


# docs = collection.query(
#     query_texts=[
#         'some girls'
#     ],
#     n_results=3
# )
# print(docs)
# # print(collection.peek(1)['metadatas'])
# # langchain_chroma = Chroma(
# #     client=persistent_client,
# #     collection_name="collection_name",
# #     embedding_function=OpenAIEmbeddings(),
# # )