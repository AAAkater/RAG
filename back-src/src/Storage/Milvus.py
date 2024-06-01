from typing import Any
from pymilvus import CollectionSchema, DataType, MilvusClient
import glob
from pathlib import Path
from langchain_community.vectorstores.milvus import Milvus as lc_milvus
from pymilvus.milvus_client.index import IndexParams

from .PrepareDatasets import prepare
from ..Embeddings.multi_qa_mpnet_base_dot_v1 import Embedding
from ..MLLM.Moondream import Moondream


class Milvus:
    uri: str = "http://127.0.0.1:19530"
    client: Any
    mllm: Any
    embedding: Any
    collection_name: str = "images"

    def __init__(self) -> None:
        self.client = MilvusClient(uri=self.uri)
        self.embedding = Embedding()
        self._InitCollection

    @property
    def _InitCollection(self) -> None:
        """初始化images集合"""
        has_collection = self.client.has_collection(
            collection_name=self.collection_name
        )
        if not has_collection:
            schema: CollectionSchema = MilvusClient.create_schema(
                auto_id=False,
                enable_dynamic_field=True,
            )
            schema.add_field(
                field_name="id",
                datatype=DataType.VARCHAR,
                max_length=256,
                is_primary=True,
            )
            schema.add_field(
                field_name="desc",
                datatype=DataType.VARCHAR,
                max_length=65535,
            )
            schema.add_field(
                field_name="desc_vec", datatype=DataType.FLOAT_VECTOR, dim=768
            )
            index_params: IndexParams = self.client.prepare_index_params()
            index_params.add_index(field_name="id")
            index_params.add_index(
                field_name="desc_vec", index_type="AUTOINDEX", metric_type="IP"
            )
            self.client.create_collection(
                collection_name="images", schema=schema, index_params=index_params
            )

    def add(self, collection_name: str, imgs_path: str):
        """将文件夹下的所有jpg后缀的图片写入数据库

        Args:
            collection_name (str): 被写入集合名
            imgs_path (str): 图片文件夹路径
        """
        self.mllm = Moondream()
        print("Preparing datasets...")
        prepare(imgs_path)
        for i, image_path in enumerate(
            glob.glob(f"{imgs_path}/**/*.jpg", recursive=True), start=1
        ):
            sha256: str = Path(image_path).stem

            if len(
                self.client.query(
                    collection_name=collection_name, filter='id == "%s"' % sha256
                )
            ):
                print(sha256, "SKIPPED")
                continue

            desc = self.mllm.answer(image_path)
            desc_vec = self.embedding.encode(desc)

            print("\033[34m" + f"序号 {i} {'DESC: '}{desc}" + "\033[0m")
            print("\033[33m" + f"{sha256=}\n" + "\033[0m")

            self.client.insert(
                collection_name=collection_name,
                data={"id": sha256, "desc": desc, "desc_vec": desc_vec},
            )

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
