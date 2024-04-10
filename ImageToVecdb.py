import os
import sys
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter, MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.document_loaders.image import UnstructuredImageLoader
from langchain_community.document_loaders import ImageCaptionLoader

# 向量数据库路径
vecdb_directory: str = os.path.join(
    os.path.dirname(os.path.abspath(sys.argv[0])), "vecdb"
)

# 存放图像摘要的文件夹的路径
docs_directory = os.path.join(os.path.dirname(
    os.path.abspath(sys.argv[0])), "docs")

# 存放图像的文件夹的路径
imgs_directory = os.path.join(os.path.dirname(
    os.path.abspath(sys.argv[0])), "imgs")


images = []
# 读取imgs文件夹下的所有png
i = 1
for root, dirs, files in os.walk(imgs_directory):
    for file in files:
        if file.endswith(".png"):
            file_path = os.path.join(root, file)
            try:
                loader = ImageCaptionLoader(file_path)
                tmp = loader.load()
                images.extend(tmp)
            except Exception as e:
                print(f"序号:{i} 加载失败")
                print(e)
            else:
                print(f"序号:{i} 已加载")
                i += 1
                print(f"metadata:{tmp[0].metadata}")
                print(f"content:{tmp[0].page_content}")

text_splitter = CharacterTextSplitter(chunk_size=10, chunk_overlap=5)
splits = text_splitter.split_documents(images)

# print(f"{len(splits)=}")
# print(splits[0])

# 存储到向量数据库
try:
    vectordb = Chroma.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        persist_directory=vecdb_directory,
    )
    # 保存到本地
    vectordb.persist()
except Exception as e:
    print("载入数据库失败")
    print(e)
else:
    print("载入数据库成功")
