from pydantic import BaseModel, EmailStr


# 🔹 Used for creating user (input)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# 🔹 Used for returning user (output)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    class Config:
        from_attributes = True   # for SQLAlchemy models


# 🔹 Used for login
class Login(BaseModel):
    email: EmailStr
    password: str