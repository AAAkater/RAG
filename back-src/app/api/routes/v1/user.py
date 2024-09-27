from fastapi import APIRouter, status

router = APIRouter()


@router.get(path="/session", status_code=status.HTTP_200_OK, summary="get session")
async def get_session():
    pass
