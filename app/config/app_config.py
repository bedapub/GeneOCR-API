import os

# APP configs
HOST = os.environ.get('HOST', 'localhost')
PORT = os.environ.get('PORT', '5000')
DEBUG = bool(int(os.environ.get('DEBUG', '0')))

LOG_LEVELS = ['DEBUG', 'INFO', 'WARN', 'WARNING', 'ERROR', 'FATAL', 'CRITICAL']
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
