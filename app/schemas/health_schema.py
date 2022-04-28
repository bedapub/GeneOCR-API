from pydantic import BaseModel, Field


class HealthStatusResponseSchema(BaseModel):
    status: str = Field('UP')
