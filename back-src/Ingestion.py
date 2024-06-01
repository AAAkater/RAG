from src.Storage.PrepareDatasets import prepare
from src.Storage.Milvus import Milvus
import os

images_path = "./images/"
name = "images"

if __name__ == "__main__":
    print("Preparing datasets...")
    try:
        db = Milvus()
    except RuntimeError as e:
        print(f"MLLM初始化失败:{e}")
        exit(code=0)
    print("Updating DB...")
    db.add(collection_name=name, imgs_path=images_path)
    # print(len(os.listdir(images_path)))
