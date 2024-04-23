from pymilvus import DataType, MilvusClient
import glob
from pathlib import Path

from Embedding import Embedding
from .PrepareDatasets import prepare
from .MLLM import Moondream


client = MilvusClient(
    uri="http://localhost:19530"
)

has_collection = client.has_collection(collection_name="images")
if not has_collection:
    schema = MilvusClient.create_schema(
        auto_id=False,
        enable_dynamic_field=True,
    )
    schema.add_field(
        field_name="id",
        datatype=DataType.VARCHAR,
        max_length=256,
        is_primary=True
    )
    schema.add_field(
        field_name="desc",
        datatype=DataType.VARCHAR,
        max_length=65535,
    )
    schema.add_field(
        field_name="desc_vec",
        datatype=DataType.FLOAT_VECTOR,
        dim=768
    )
    index_params = client.prepare_index_params()
    index_params.add_index(
        field_name="id"
    )
    index_params.add_index(
        field_name="desc_vec",
        index_type="AUTOINDEX",
        metric_type="IP"
    )
    client.create_collection(
        collection_name="images",
        schema=schema,
        index_params=index_params
    )

print("Preparing datasets...")
prepare('./Storage/Datasets')

print("Loading models...")
mllm = Moondream()
embedding = Embedding()

print("Updating DB...")
for image_path in glob.glob('./Storage/Datasets/**/*.jpg', recursive=True):
    sha256 = Path(image_path).stem

    if len(client.query("images", 'id == "%s"' % sha256)):
        print(sha256, "SKIPPED")
        continue

    exists, _ = client.has_entity(
        collection_name="images",
        entity_ids=[sha256],
        field_name="id"
    )
    if exists[0]:
        continue

    desc = mllm.answer(image_path)
    desc_vec = embedding.encode(desc)

    print(sha256, " DESC. ", desc[:50])

    client.insert("images", {
        "id": sha256,
        "desc": desc,
        "desc_vec": desc_vec
    })
