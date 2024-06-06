import glob
import os
from pathlib import Path
from pprint import pp
from typing import Any

from app.metadata import audio, document, image, video
from app.utils.Embeddings.multi_qa_mpnet_base_dot_v1 import Embedding
from app.utils.MLLM.Moondream import Moondream
from app.utils.sha256.image_name_to_sha256 import prepare
from langchain_community.vectorstores.milvus import Milvus as lc_milvus
from pymilvus import MilvusClient


class Database:
    uri: str = "http://127.0.0.1:19530"
    collection_names: list[str] = ["images", "audio", "document", "video"]

    def __init__(self) -> None:
        self.client = MilvusClient(uri=self.uri)
        self.embedding = Embedding()

    def insert_image(self, image_name: str):
        """将图片转换成向量再写入数据库

        Args:
            image_name (str): 图片名
        """
        collection_name = "images"
        path: str = os.path.join(os.path.dirname(image.__file__), image_name)

        return

    def insert_document(self, document_name: str):
        """将文档转换成向量再写入数据库

        Args:
            document_name (str): _description_
        """
        collection_name = "document"

        return

    def insert_audio(self, audio_name: str):
        """将音频转换成向量再写入数据库

        Args:
            audio_name (str): _description_
        """
        collection_name = "audio"

        return

    def insert_video(self, video_name: str):
        """将视频转换成向量再写入数据库

        Args:
            video_name (str): _description_
        """
        collection_name = "video"

        return

    def search(self, query: str):
        """向量搜索

        Args:
            query (str): 特征

        Returns:
            _type_:
        """
        res = self.client.search(
            collection_name=self.collection_names[0],
            data=self.embedding.embed_document([query]),
            output_fields=["id", "desc"],
            limit=5,
        )

        return res

    @property
    def as_retriever(self):
        images_collection = lc_milvus(
            embedding_function=self.embedding,
            collection_name=self.collection_name,
            connection_args={"uri": self.uri},
            text_field="desc",
            vector_field="desc_vec",
            primary_field="id",
        )
        return images_collection.as_retriever(search_type="mmr", search_kwargs={"k": 5})


if __name__ == "__main__":
    database = Database()
    res = database.search(query="flower")

    pp(res)
