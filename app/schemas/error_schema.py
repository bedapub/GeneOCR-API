from pydantic.fields import Field
from pydantic.main import BaseModel


class ErrorSchema(BaseModel):
    message: str = Field(description='Error message')
