from datetime import datetime, timedelta, timezone

from app.core.config import settings
from app.db.database import get_db_session
from app.db.models.user import User
from app.model import TokenPayLoad
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from jwt.exceptions import InvalidTokenError
from pydantic import ValidationError

ALGORITHM = "HS256"
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_VER_STR}/login/access-token"
)


def create_access_token(subject: str) -> str:
    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode = TokenPayLoad(
        exp=expire,
        sub=str(subject),
    ).model_dump()
    encode_jwt: str = jwt.encode(
        claims=to_encode,
        key=settings.SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return encode_jwt


def get_current_user(token: str):

    session = next(get_db_session())
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        token_data = TokenPayLoad(**payload)
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无权限",
        )

    db_user = session.get(
        User,
        token_data.sub,
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无权限",
        )
    return db_user
