from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_usecase, get_current_user_id
from app.schemas.auth import RegisterRequest, TokenResponse
from app.schemas.user import UserPublic
from app.usecases.auth import AuthUseCase

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserPublic)
async def register(data: RegisterRequest,  auth_service: AuthUseCase = Depends(get_auth_usecase)):
    return await auth_service.register_user(data)

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthUseCase = Depends(get_auth_usecase)):
    token = await auth_service.login_for_token(form_data.username, form_data.password)
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserPublic)
async def get_me(current_user_id: int = Depends(get_current_user_id), auth_service: AuthUseCase = Depends(get_auth_usecase)):
    return await auth_service.get_user_profile(current_user_id)