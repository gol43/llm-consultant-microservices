from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

Password = Annotated[str, Field(min_length=4, max_length=16)]

class RegisterRequest(BaseModel):
    email: EmailStr
    password: Password 

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"