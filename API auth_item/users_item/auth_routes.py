from jwt.exceptions import InvalidTokenError
from fastapi import (
    APIRouter,
    Depends,
    Form,
    HTTPException,
    status,
)
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database_config import utils as auth_utils
from .schemas import TokenInfo, UserSchema
from .models import Base, UserModel
from database_config.database import get_async_session, engine



oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login/",
)


router = APIRouter(tags=['auth']) 


Base.metadata.create_all(bind=engine)


def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    db: Session = Depends(get_async_session),
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
    )
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not auth_utils.validate_password(password=password, hashed_password=user.password):
        raise unauthed_exc
    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User inactive",
        )
    return user


def register_user(
    user_data: UserSchema,
    db: Session = Depends(get_async_session),
):
    existing_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )

    hashed_password = auth_utils.hash_password(user_data.password)
    new_user = UserModel(username=user_data.username, password=hashed_password, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    jwt_payload = {
        "sub": new_user.username,
        "username": new_user.username,
        "email": new_user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


def get_current_token_payload(
    token: str = Depends(oauth2_scheme),
) -> dict:
    try:
        payload = auth_utils.decode_jwt(
            token=token,
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token error: {e}",
        )
    return payload


def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload), db: Session = Depends(get_async_session)
) -> UserModel:
    username: str | None = payload.get("sub")
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalid (user not found)",
    )


def get_current_active_auth_user(
    user: UserModel = Depends(get_current_auth_user),
):
    if user.active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User inactive",
    )


@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(
    user: UserModel = Depends(validate_auth_user),
):
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer",
    )


@router.post("/register", response_model=TokenInfo)
def register_user_and_issue_jwt(
    user: UserModel = Depends(register_user),
):
    return user


@router.get("/users/me")
def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: UserModel = Depends(get_current_active_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
    }
