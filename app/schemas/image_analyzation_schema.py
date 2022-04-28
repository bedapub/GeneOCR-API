from typing import Any
from pydantic import BaseModel, Field

class ImageAnalyzationRequestModel(BaseModel):
    image: str = Field(
        ...,
        description='BASE64 string of image'
    )
    
    
class ImageAnalyzationResponseModel(BaseModel):
    status: str = Field(
        ...,
        desciption='Status of analyzation'
    )
    text: Any = Field(
        ...,
        description='Analyzed text from image'
    )
