from app.core.exceptions import InvalidCredentialsError, UserAlreadyExistsError, UserNotFoundError
from app.core.security import create_access_token, hash_password, verify_password
from app.db.models import User
from app.repositories.users import UserRepository
from app.schemas.auth import RegisterRequest


class AuthUseCase:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def register_user(self, data: RegisterRequest) -> User:
        existing_user = await self.user_repo.get_by_email(data.email)
        if existing_user:
            raise UserAlreadyExistsError()
        
        new_user = User(
            email=data.email,
            password_hash=hash_password(data.password),
            role="user"
        )
        return await self.user_repo.create(new_user)

    async def login_for_token(self, email: str, password: str) -> str:
        user = await self.user_repo.get_by_email(email)
        
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsError()

        token_data = {"sub": str(user.id), "role": user.role}
        return create_access_token(token_data)

    async def get_user_profile(self, user_id: int) -> User:
        user = await self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundError()
        return user