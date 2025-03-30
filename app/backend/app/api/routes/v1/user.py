from datetime import datetime

from app.db.crud.user import create_user, get_user_by_email
from app.db.database import SessionDep
from app.db.models.user import UserRegister
from app.model import ResponseBase, UserRegisterBody
from app.utils.log import logger
from fastapi import APIRouter, HTTPException, status
from pydantic import validate_email
from pydantic_core import PydanticCustomError

router = APIRouter()


@router.post(
    path="/user",
    status_code=status.HTTP_200_OK,
    response_model=ResponseBase,
    summary="注册新用户",
)
async def create_new_user(
    *,
    session: SessionDep,
    new_user_info: UserRegisterBody,
) -> ResponseBase:

    # 校验邮箱格式
    try:
        _ = validate_email(value=new_user_info.email)
    except PydanticCustomError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="邮箱格式错误",
        )

    # 查询用户是否已经存在
    user = get_user_by_email(
        session=session,
        email=new_user_info.email,
    )
    if user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户已存在",
        )

    # 写入数据库中
    try:
        create_user(
            session=session,
            new_user=UserRegister(
                email=new_user_info.email,
                password=new_user_info.password,
                create_time=datetime.now(),
            ),
        )
    except Exception as e:
        logger.error(msg=e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="服务器内部错误",
        )

    return ResponseBase()
