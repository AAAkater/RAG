from app.db.crud.user import authenticate_user
from app.db.database import SessionDep
from app.model import ResponseBase, TokenItem, UserLoginBody
from app.utils.log import logger
from app.utils.redis_api import redis_client
from app.utils.security import create_access_token
from fastapi import APIRouter, HTTPException, status

router = APIRouter()


@router.post(
    path="/login",
    status_code=status.HTTP_200_OK,
    summary="用户登录",
    response_model=ResponseBase[TokenItem],
)
async def user_login(
    *,
    session: SessionDep,
    user_info: UserLoginBody,
):
    # 校验图片验证码
    code = redis_client.get(user_info.captcha_id)
    if (
        # (not code)
        code != user_info.captcha_code
        or code.lower() != user_info.captcha_code
    ):
        return ResponseBase(code="1", msg="验证码错误")
    # 从数据库中查询该用户
    db_user = authenticate_user(
        session=session,
        email=user_info.username,
        password=user_info.password,
    )
    if not db_user:
        return ResponseBase(code="2", msg="密码错误")
    token = create_access_token(db_user.id)

    return ResponseBase[TokenItem](data=TokenItem(access_token=token))
