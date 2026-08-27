from pydantic import BaseModel


class LoginDTO(BaseModel):
    email: str
    password: str


class LoginDataDTO(BaseModel):
    login: LoginDTO


class LoginRequestDTO(BaseModel):
    message: str
    data: LoginDataDTO