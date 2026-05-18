from pydantic import BaseModel, EmailStr, Field



class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

class UserRegister(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str

class ChatRequest(BaseModel):
    user_id: str
    query: str

class Response(BaseModel):
    message : str

class UploadResponse(BaseModel):
    filename : str
    indexed: bool
    chunks : int

class ErrorResponse(BaseModel):
    error : str

class ChatResponse(BaseModel):
    answer : str
