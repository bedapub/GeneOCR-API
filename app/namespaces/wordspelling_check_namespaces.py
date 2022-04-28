from fastapi.routing import APIRouter
from fastapi import status

from schemas.health_schema import HealthStatusResponseSchema

wordspelling_check_namespace = APIRouter(prefix='/spelling')


@wordspelling_check_namespace.post(
    '/suggestions',
    description='Get service health status',
    status_code=status.HTTP_200_OK,
)
def health_endpoint():
    return ''
