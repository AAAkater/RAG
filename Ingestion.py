from pymilvus import DataType, MilvusClient
import glob
from pathlib import Path

from src.MLLM.Moondream import Moondream
from src.Embeddings.multi_qa_mpnet_base_dot_v1 import Embedding
from src.Storage.PrepareDatasets import prepare
from src.Storage.Milvus import Milus

images_path = "./imgs/girls"
name = "images"

if __name__ == "__main__":
    print("Preparing datasets...")
    prepare(images_path)
    try:
        db = Milus()
    except RuntimeError as e:
        print(f"MLLM初始化失败:{e}")
        exit(code=0)
    print("Updating DB...")
    db.add(collection_name=name, imgs_path=images_path)
