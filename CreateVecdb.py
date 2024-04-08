

import glob
import os
from langchain_community.vectorstores import chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.document_loaders import DirectoryLoader
from langchain_community.document_loaders import unstructured
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
vecdb_path = 'F:\\Desktop\\vsc\\python\\RAG\\vecdb'


# 获取当前目录
current_dir = os.getcwd()

docs_dir = os.path.join(current_dir, 'docs')
txt_files = glob.glob(os.path.join(docs_dir, '*.txt'))


def load_txt_file(txt_file):
    loader = unstructured(os.path.join(work_dir, txt_file))
    docs = loader.load()
    print(docs[0].page_content[:100])
    return docs


def load_txt_splitter(txt_file, chunk_size=200, chunk_overlap=20):
    docs = load_txt_file(txt_file)
    text_splitter = CharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    split_docs = text_splitter.split_documents(docs)
    # 默认展示分割后第一段内容
    print('split_docs[0]: ', split_docs[0])
    return split_docs


splitters = []
# docs = []
for file in txt_files:
    with open(file, 'r') as f:
        content = f.read()

        # print(content)


for splitter in splitters:
    print(splitter)
    print(len(splitter))


sent = "你好"

# vecdb = chroma.Chroma(
#     collection_name=sent,
#     embedding_function=OpenAIEmbeddings(),
#     persist_directory=vecdb_path
# )

# vecdb = chroma.Chroma(

# ).afrom_documents()
