from fastapi.routing import APIRouter
from fastapi import status

from schemas.health_schema import HealthStatusResponseSchema

health_namespace = APIRouter(prefix='/health')


@health_namespace.get(
    '',
    description='Get service health status',
    status_code=status.HTTP_200_OK,
    response_model=HealthStatusResponseSchema
)
def health_endpoint():
    return HealthStatusResponseSchema()
