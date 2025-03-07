import os
from dotenv import load_dotenv

FOLDER = os.path.dirname(__file__)

load_dotenv(f'{FOLDER}/.env')

# ===== Logging =====

import logging  # noqa: E402


LOGGING_MESSAGE_FORMAT = '[%(levelname)s @ %(asctime)s] %(message)s'
LOGGING_DATE_FORMAT = '%H:%M:%S'


def add_logger_file_handler(
    logger: logging.Logger,
    level: int | str = logging.DEBUG,
) -> None:
    from datetime import datetime

    logs_folder = f'{FOLDER}/logs/{datetime.now().strftime("%Y.%m.%d")}'
    log_name = datetime.now().strftime('%H-%M-%S')
    os.makedirs(logs_folder, exist_ok=True)
    handler = logging.FileHandler(f'{logs_folder}/{log_name}.log')
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            fmt=LOGGING_MESSAGE_FORMAT,
            datefmt=LOGGING_DATE_FORMAT,
        )
    )
    logger.addHandler(handler)


def add_logger_stdout_handler(
    logger: logging.Logger,
    level: int | str = logging.DEBUG,
) -> None:
    import sys

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            fmt=LOGGING_MESSAGE_FORMAT,
            datefmt=LOGGING_DATE_FORMAT,
        )
    )
    logger.addHandler(handler)


logger = logging.getLogger('transformer')
logger.setLevel(logging.DEBUG)
add_logger_file_handler(logger)
add_logger_stdout_handler(logger)

# ===== Model =====

from openai import AsyncOpenAI  # noqa: E402

MODEL_API_KEY = os.environ.get('MODEL_API_KEY')
MODEL_NAME = os.environ.get('MODEL_NAME')

if MODEL_API_KEY is None:
    logger.warning(
        'Environment variable `MODEL_API_KEY` is not set. '
        'Trying to call AI methods will result in an error.'
    )
if MODEL_NAME is None:
    logger.warning(
        'Environment variable `MODEL_NAME` is not set. '
        'Trying to call AI methods will result in an error.'
    )

client = AsyncOpenAI(
    base_url='https://integrate.api.nvidia.com/v1',
    api_key=MODEL_API_KEY,
)
