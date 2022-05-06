import traceback

from fastapi import FastAPI, APIRouter
from namespaces.health_namespace import health_namespace
from namespaces.analyzation_namespace import analyzation_namespace
from namespaces.wordspelling_check_namespaces import wordspelling_check_namespace
from namespaces.image_helper_namespace import image_helper_namespace

_API_TAGS_METADATA = [
    {
        'name': 'health',
        'description': 'Service health status'
    },
    {
        'name': 'analyze',
        'description': 'Image analyzation'
    },
    {
        'name': 'spelling',
        'description': 'Check word spelling'
    },
    {
        'name': 'image-helper',
        'description': 'Helper functions for images'
    }
]


def init_api(app: FastAPI):
    app.openapi_tags = _API_TAGS_METADATA
    api_v1 = APIRouter(prefix='/v1')
    api_v1.include_router(health_namespace, tags=['health'])
    api_v1.include_router(analyzation_namespace, tags=['analyze'])
    api_v1.include_router(wordspelling_check_namespace, tags=['spelling'])
    api_v1.include_router(image_helper_namespace, tags=['image-helper'])
    app.include_router(api_v1)
    _include_error_handlers(app)

 
def _include_error_handlers(app: FastAPI):
    """
    @app.exception_handler(StarletteHTTPException)
    def handle_starlette_http_exception(_, error: StarletteHTTPException):
        _log_error_with_stack_trace(error)
        status_code = error.status_code or status.HTTP_500_INTERNAL_SERVER_ERROR
        return _generate_error_json_response(str(error.detail), status_code)

    @app.exception_handler(InvalidInputError)
    def handle_invalid_input_error(_, error):
        _log_error_with_stack_trace(error)
        return _generate_error_json_response(str(error), status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(AuthorizationError)
    def handle_authorization_error(_, error):
        _log_error_with_stack_trace(error)
        return _generate_error_json_response(str(error), status.HTTP_401_UNAUTHORIZED)

    @app.exception_handler(AuthenticationError)
    def handle_authorization_error(_, error):
        _log_error_with_stack_trace(error)
        return _generate_error_json_response(str(error), status.HTTP_403_FORBIDDEN)

    @app.exception_handler(InvalidSmartsError)
    def handle_invalid_smarts_error(_, error):
        _log_error_with_stack_trace(error)
        return _generate_error_json_response(str(error), status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(Exception)
    def handle_general_error(_, error):
        _log_error_with_stack_trace(error)
        return _generate_error_json_response(str(error), status.HTTP_500_INTERNAL_SERVER_ERROR)


def _log_error_with_stack_trace(error: Exception):
    stack_trace = "".join(
        traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
    )
    error_message = str(error)
    if isinstance(error, StarletteHTTPException):
        error_message = error.detail

    logger.exception(f'{str(error_message)}\n{stack_trace}')


def _generate_error_json_response(error_message: str, status_code: int) -> JSONResponse:
    return JSONResponse(content={'message': error_message}, status_code=status_code)
 """