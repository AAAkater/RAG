import os
import sys
from typing import List
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_community.docstore.document import Document
from src.MLLM import moondream
from src.Vectordb import vecdb
from src.ToPng import to_png

# 存放图片文件夹的位置
images_path = "./imgs/girls"

if __name__ == "__main__":

    try:
        mllm = moondream()
    except RuntimeError as e:
        print(e)
    else:
        print(f"MLLM初始化成功")
    collection = vecdb(collection_name="langchain")
    # to_png(images_path)
    for i, file_name in enumerate(os.listdir(images_path), start=1):
        file_path: str = f"{images_path}/{file_name}"
        try:
            doc: Document = mllm.answer(file_path)
            collection.add(doc)
            print(file_path)
        except Exception as e:
            print(f"图片序号:{i} 加载失败")
            print(e)
        else:
            print(f"图片序号:{i} 已加载")
            # print(f"metadata:{doc.metadata}")
            # print(f"content:{doc.page_content}")
