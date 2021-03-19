import os
from loguru import logger

logger.add('gebug.json', format="{time} {level} {message}", level='ERROR', rotation='20 KB', compression='zip', serialize=True, backtrace=True, diagnose=False)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))