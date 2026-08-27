from pydantic import BaseModel, EmailStr, Field
 
 
class RegistrationData(BaseModel):
    name: str
    email: EmailStr
    contact: str = Field(
        pattern=r"^[6-9][0-9]{9}$",
        description="A 10-digit mobile number starting with 6, 7, 8, or 9",
    )
    password: str = Field(min_length=5)
 
 
class RegistrationRequestData(BaseModel):
    registration: RegistrationData
 
 
class RegistrationRequestDTO(BaseModel):
    data: RegistrationRequestData
 
 
class RegistrationResponseDTO(BaseModel):
    message: str
    data: dict
    access_token: str
    token_type: str = "bearer"