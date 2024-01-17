from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen


class CreateUser(BaseModel):
    # username: str = Field(min_length=3, max_length=20)
    username: Annotated[str, MinLen(3), MaxLen(20)]
    email: EmailStr


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)
    username: str
    password: bytes
    email: Optional[EmailStr] = None
    active: bool = True
