import os
import sys
from typing import List
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_community.docstore.document import Document
from src.MLLM import MLLM_model
from src.Vectordb import vecdb

# 存放图片文件夹的位置
images_path = "./imgs/"

if __name__ == "__main__":

    MLLM = MLLM_model()
    collection = vecdb(collection_name="langchain")
    text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=5)

    i = 1
    for root, dirs, files in os.walk(images_path):
        for file in files:
            if file.endswith(".png"):
                file_path: str = os.path.join(root, file)
                try:
                    doc: Document = MLLM.answer(file_path)
                    collection.add(doc)
                except Exception as e:
                    print(f"图片序号:{i} 加载失败")
                    print(e)
                else:
                    print(f"图片序号:{i} 已加载")
                    i += 1
                    print(f"metadata:{doc.metadata}")
                    print(f"content:{doc.page_content}")
