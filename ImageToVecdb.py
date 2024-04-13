import os
import sys
from typing import List
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter, MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders.image import UnstructuredImageLoader
from langchain_community.document_loaders import ImageCaptionLoader
from langchain_community.docstore.document import Document
from PIL import Image
from src.MLLM import MLLM_model
from src.Vectordb import vecdb

# 向量数据库路径
vecdb_directory: str = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0])), "database"
)

# 存放图像摘要的文件夹的路径
docs_directory: str = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0])), "docs"
)

# 存放图像的文件夹的路径
imgs_directory: str = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0])), "imgs"
)


if __name__ == "__main__":

    MLLM = MLLM_model()
    db = vecdb(collection_name="langchain")
    text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=5)

    images = []
    i = 1
    for root, dirs, files in os.walk(imgs_directory):
        for file in files:
            if file.endswith(".png"):
                file_path: str = os.path.join(root, file)
                try:
                    doc: Document = MLLM.answer(file_path)
                    db.add(doc)
                except Exception as e:
                    print(f"图片序号:{i} 加载失败")
                    print(e)
                else:
                    print(f"图片序号:{i} 已加载")
                    i += 1
                    print(f"metadata:{doc.metadata}")
                    print(f"content:{doc.page_content}")

    # print(f"{len(splits)=}")
    # print(splits[0])

    # 存储到向量数据库
    # try:
    #     vectordb = Chroma.from_documents(
    #         documents=splits,
    #         embedding=OpenAIEmbeddings(),
    #         persist_directory=vecdb_directory,
    #     )
    #     # 保存到本地
    #     vectordb.persist()
    # except Exception as e:
    #     print("载入数据库失败")
    #     print(e)
    # else:
    #     print("载入数据库成功")
