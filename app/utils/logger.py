from loguru import logger
import os
from sys import stdout


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logger.remove()
logger.add(stdout, level=LOG_LEVEL)
logger.add("logs/app_{time}.log", rotation="10 MB", level=LOG_LEVEL)

