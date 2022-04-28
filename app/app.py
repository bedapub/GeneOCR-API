import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import init_api
from config.app_config import DEBUG, PORT, HOST
from logger import configure_logger, logger

app = FastAPI(
    title='GeneRead API',
    description='GeneRead App backend endpoints',
    version='{{VERSION}}',
    debug=DEBUG,
    docs_url='/',
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

configure_logger(app, logger)
init_api(app)

print(f'--- Service is starting on {HOST}:{PORT} ---')
if __name__ == '__main__':
    uvicorn.run('app:app', host=HOST, port=PORT, debug=DEBUG, reload=DEBUG)
