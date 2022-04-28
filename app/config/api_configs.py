from starlette import status

from schemas.error_schema import ErrorSchema

HTTP_400_API_RESPONSE_MODEL = {
    status.HTTP_400_BAD_REQUEST: {'model': ErrorSchema, 'description': 'Invalid argument/s'}
}
HTTP_401_API_RESPONSE_MODEL = {
    status.HTTP_401_UNAUTHORIZED: {'model': ErrorSchema, 'description': 'Invalid authentication'}
}
HTTP_403_API_RESPONSE_MODEL = {
    status.HTTP_403_FORBIDDEN: {'model': ErrorSchema, 'description': 'Missing authentication'}
}
HTTP_404_API_RESPONSE_MODEL = {
    status.HTTP_404_NOT_FOUND: {'model': ErrorSchema, 'description': 'Endpoint couldn\'t be found'}
}
HTTP_422_API_RESPONSE_MODEL = {
    status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': ErrorSchema, 'description': 'Invalid argument/s'}
}
HTTP_500_API_RESPONSE_MODEL = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': ErrorSchema, 'description': 'Unexpected error occurred'}
}


COMMON_API_RESPONSE_MODELS = {
    **HTTP_400_API_RESPONSE_MODEL,
    **HTTP_401_API_RESPONSE_MODEL,
    **HTTP_403_API_RESPONSE_MODEL,
    **HTTP_422_API_RESPONSE_MODEL,
    **HTTP_500_API_RESPONSE_MODEL
}
