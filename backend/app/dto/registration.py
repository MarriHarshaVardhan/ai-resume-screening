from pydantic import BaseModel, Field


class RegistrationData(BaseModel):
    name: str
    email: str
    contact: str
    password: str = Field(min_length=8)


class RegistrationRequestData(BaseModel):
    registration: RegistrationData


class RegistrationRequestDTO(BaseModel):
    data: RegistrationRequestData


class RegistrationResponseDTO(BaseModel):
    message: str
    data: dict
