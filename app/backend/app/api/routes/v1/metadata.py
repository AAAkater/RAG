from app.model import ResponseBase, UploadMetadataItem
from fastapi import APIRouter, HTTPException, UploadFile, status

isDeprecated = False


router = APIRouter()


@router.post(
    path="/metadata/{knowledge_base_name}",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase[UploadMetadataItem],
    summary="upload metadata files",
    deprecated=isDeprecated,
)
async def upload_metadata(knowledge_base_name: str, files: list[UploadFile]):
    # Verify that the knowledge base exists
    if knowledge_base_name not in ["vue", "react"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The knowledge base does not exist:{knowledge_base_name}",
        )

    filenames = []
    for file in files:
        # Write metadata locally
        try:
            with open(file.filename, "wb") as f:
                content = await file.read()
                f.write(content)
        except Exception as e:
            print(e)
        filenames.append(file.filename)
    return ResponseBase[UploadMetadataItem](
        code="0",
        msg="ok",
        data=UploadMetadataItem(
            knowledge_base_name=knowledge_base_name, files=filenames
        ),
    )


@router.put(
    path="/metadata/{knowledge_base_name}/{metadata_id}",
    status_code=status.HTTP_200_OK,
    summary="",
)
async def update_metadata(knowledge_base_name: str, metadata_id: str):
    return


@router.get(
    path="/metadata/{knowledge_base_name}", status_code=status.HTTP_200_OK, summary=""
)
async def get_metadata_items(knowledge_base_name: str):

    return


@router.get(
    path="/metadata/{knowledge_base_name}/{metadata_id}",
    status_code=status.HTTP_200_OK,
    summary="",
)
async def get_single_metadata(knowledge_base_name: str, metadata_id: str):
    return


@router.delete(
    path="/metadata/{knowledge_base_name}/{metadata_id}",
    status_code=status.HTTP_200_OK,
    summary="",
)
async def del_metadata(knowledge_base_name: str, metadata_id: str):
    return
