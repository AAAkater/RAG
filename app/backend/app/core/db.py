import sys
from pprint import pp

from app.core.log import logger
from pymilvus import (
    Collection,
    CollectionSchema,
    DataType,
    FieldSchema,
    MilvusClient,
    connections,
)
from pymilvus.milvus_client.index import IndexParams

fields: list[FieldSchema] = [
    FieldSchema(
        name="id",
        dtype=DataType.VARCHAR,
        is_primary=True,
        max_length=256,
        description="primary id",
    ),
    FieldSchema(
        name="desc", dtype=DataType.VARCHAR, max_length=65535, description="文本描述"
    ),
    FieldSchema(
        name="desc_vec", dtype=DataType.FLOAT_VECTOR, dim=768, description="向量"
    ),
    FieldSchema(
        name="metadata", dtype=DataType.VARCHAR, max_length=65535, description="元数据"
    ),
]
schema = CollectionSchema(
    fields=fields,
    auto_id=False,
    enable_dynamic_field=True,
)


def init_db(uri: str = "http://127.0.0.1:19530"):
    client = MilvusClient(uri)

    collection_names = ["image", "audio", "document", "video"]

    has_collections: list[tuple[bool, str]] = [
        (client.has_collection(name), name) for name in collection_names
    ]

    for has_collection, name in has_collections:
        if not has_collection:

            logger.info(f"{name} 集合不存在")

            index_params: IndexParams = client.prepare_index_params()
            index_params.add_index(
                field_name="desc_vec", index_type="AUTOINDEX", metric_type="IP"
            )
            client.create_collection(
                collection_name=name, schema=schema, index_params=index_params
            )
            logger.info(f"{name} 集合创建成功")
        else:
            logger.info(f"{name} 集合已存在")
    client.close()


if __name__ == "__main__":

    connections.connect()
    new_collection = Collection(name="image")

    new_collection.load()
    pp(new_collection.query(expr="", output_fields=["id", "metadata", "desc"], limit=5))
