import glob
import os
import uuid
from pathlib import Path
from pprint import pp
from typing import Any, Literal, Tuple

import app.metadata.audio as audio
import app.metadata.document as document
import app.metadata.image as image
import app.metadata.video as video
from app.utils.Embeddings.multi_qa_mpnet_base_dot_v1 import Embedding
from app.utils.MLLM.audio_model import WhisperLargeV3
from app.utils.MLLM.image_model import Moondream
from app.utils.Tokenizer.pdf_splitter import pdf_splitter
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain_community.vectorstores.milvus import Milvus as lc_milvus
from langchain_core.vectorstores import VectorStoreRetriever
from pymilvus import Collection, MilvusClient, connections


class Database:
    uri: str = "http://127.0.0.1:19530"
    collection_names: list[str] = ["image", "document", "audio", "video"]

    def __init__(self) -> None:
        self.__client = MilvusClient(uri=self.uri)
        self.__embedding_model = Embedding()
        self.__image_model = Moondream()
        self.__audio_model = WhisperLargeV3()

    @property
    def as_retriever(self):
        images_collection = lc_milvus(
            embedding_function=self.__embedding_model,
            collection_name=self.collection_names[0],
            connection_args={"uri": self.uri},
            primary_field="id",
            text_field="desc",
            vector_field="desc_vec",
        )
        return images_collection.as_retriever(search_type="mmr", search_kwargs={"k": 5})

    def search(self, query: str):
        """向量搜索

        Args:
            query (str): 特征

        Returns:
            _type_:
        """
        res = self.__client.search(
            collection_name=self.collection_names[0],
            data=self.__embedding_model.embed_documents([query]),
            output_fields=["id", "desc"],
            limit=5,
        )

        return res

    def insert_image(self, uuid: str, new_name: str, old_name: str):
        """将图片转换成向量并存入数据库

        Args:
            uuid (str): _description_
            new_name (str): _description_
            old_name (str): _description_
        """

        path: str = os.path.join(os.path.dirname(image.__file__), new_name)
        desc: str = self.__image_model.answer(path)
        desc_vec = self.__embedding_model.encode(desc)
        self.__client.insert(
            collection_name="image",
            data={"id": uuid, "desc": desc, "desc_vec": desc_vec, "metadata": old_name},
        )
        return

    def insert_document(self, file_name: str):
        """将文档转换成向量再写入数据库

        Args:
            uuid (str): _description_
            new_name (str): _description_
            old_name (str): _description_
        """
        path: str = os.path.join(os.path.dirname(document.__file__), file_name)
        loader = PyPDFLoader(path)
        pages = loader.load_and_split(pdf_splitter)

        embeddings = self.__embedding_model.embed_documents(
            [page.page_content for page in pages]
        )
        print(len(embeddings))
        for embedding, page in zip(embeddings, pages):
            self.__client.insert(
                collection_name="document",
                data={
                    "id": str(uuid.uuid4()),
                    "desc": page.page_content,
                    "desc_vec": embedding,
                    "metadata": file_name,
                },
            )
        return

    def insert_audio(self, file_name: str):
        """将音频转换成向量再写入数据库

        Args:
            audio_name (str): _description_
        """
        path: str = os.path.join(os.path.dirname(audio.__file__), file_name)
        answer: str = self.__audio_model.answer(path)

        texts = pdf_splitter.split_text(answer)
        embeddings = self.__embedding_model.embed_documents(texts)

        for text, embedding in zip(texts, embeddings):
            self.__client.insert(
                collection_name="audio",
                data={
                    "id": str(uuid.uuid4()),
                    "desc": text,
                    "desc_vec": embedding,
                    "metadata": file_name,
                },
            )
        return

    def insert_video(self, video_name: str):
        """将视频转换成向量再写入数据库

        Args:
            video_name (str): _description_
        """
        collection_name = "video"

        return

    def search_image_metadata(self, image_id: str):
        metadata = self.__client.get(
            collection_name=self.collection_names[0],
            ids=image_id,
            output_fields=["metadata"],
        )
        if len(metadata) == 0:
            return (False, "")
        return (True, metadata[0]["metadata"])

    def search_document_metadata(self, document_id: str):
        metadata = self.__client.get(
            collection_name=self.collection_names[1],
            ids=document_id,
            output_fields=["metadata"],
        )
        if len(metadata) == 0:
            return (False, "")
        return (True, metadata[0]["metadata"])

    def search_audio_metadata(self, audio_id: str):
        metadata = self.__client.get(
            collection_name=self.collection_names[2],
            ids=audio_id,
            output_fields=["metadata"],
        )
        if len(metadata) == 0:
            return (False, "")
        return (True, metadata[0]["metadata"])

    def search_video_metadata(self, video_id: str):
        metadata = self.__client.get(
            collection_name=self.collection_names[3],
            ids=video_id,
            output_fields=["metadata"],
        )
        if len(metadata) == 0:
            return (False, "")
        return (True, metadata[0]["metadata"])


database = Database()

if __name__ == "__main__":

    # res = database.search(query="flower")

    # retriever: VectorStoreRetriever = database.as_retriever

    # pp(retriever.invoke(input="flower"))

    connections.connect("default", host="localhost", port="19530")
    # 集合名称
    collection_name = "image"

    # 要删除的主键 ID
    primary_key_id = "bab5013a-c58d-4ada-bdf8-ffad7e326d3b"  # 替换为你的主键 ID

    # 获取集合对象
    collection = Collection(name=collection_name)

    # 删除指定主键 ID 的数据
    collection.delete(expr=f'id in ["{primary_key_id}"]')

    # 提交删除操作
    collection.load()
