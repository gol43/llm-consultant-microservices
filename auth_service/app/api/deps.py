from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError
from app.db.session import AsyncSessionLocal
from app.repositories.users import UserRepository
from app.usecases.auth import AuthUseCase

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

async def get_auth_usecase(session: AsyncSession = Depends(get_db)) -> AuthUseCase:
    return AuthUseCase(UserRepository(session))

async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET, 
            algorithms=[settings.JWT_ALG]
        )
        user_id_str: str = payload.get("sub")
        
        if user_id_str is None:
            raise InvalidTokenError()
            
        return int(user_id_str)
        
    except ExpiredSignatureError:
        raise TokenExpiredError()
        
    except (JWTError, ValueError):
        raise InvalidTokenError()