from fastapi import APIRouter, HTTPException, UploadFile, status

from app.model import State404Response, UploadMetadataResponse

version = "v1"
isDeprecated = False


router = APIRouter()


@router.post(
    path=f"/api/{version}" + "/metadata/{knowledge_base_name}",
    status_code=status.HTTP_200_OK,
    response_model=UploadMetadataResponse,
    tags=["metadata"],
    summary="upload metadata files",
    deprecated=isDeprecated,
)
async def upload_metadata(
    knowledge_base_name: str, files: list[UploadFile]
) -> UploadMetadataResponse:
    # Verify that the knowledge base exists
    if knowledge_base_name not in ["vue", "react"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=State404Response(
                code="0",
                msg=f"The knowledge base does not exist:{knowledge_base_name}",
                data=None,
            ).model_dump(),
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
    return UploadMetadataResponse(
        code="0",
        msg="ok",
        data={"knowledge_base_name": knowledge_base_name, "files": filenames},
    )
