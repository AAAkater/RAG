

import os
import sys
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter, MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings

# 向量数据库路径
vecdb_directory: str = os.path.join(os.path.dirname(
    os.path.abspath(sys.argv[0])), 'vecdb')

# 存放图像摘要的文件夹的路径
docs_directory = os.path.join(os.path.dirname(
    os.path.abspath(sys.argv[0])), 'docs')

text_splitter = CharacterTextSplitter(
    chunk_size=200, chunk_overlap=20)

Docs = []
# 读取docs文件夹下的所有txt
for root, dirs, files in os.walk(docs_directory):
    for file in files:
        if file.endswith('.txt'):
            file_path = os.path.join(root, file)
            loader = UnstructuredFileLoader(file_path)
            Docs.extend(loader.load())

splits = text_splitter.split_documents(Docs)
print(len(splits))

# 存储到向量数据库
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings(),
    persist_directory=vecdb_directory
)
# 保存到本地
vectordb.persist()
