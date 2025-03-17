from typing import Any
from datetime import datetime
import json
from string import (
    ascii_lowercase,
    digits,
)

from .. import config
from ..config import (
    FOLDER,
    logger,
)


__all__ = [
    'config',
    'logger',
    'get_schema_file',
    'query_interactive_args',
    'start_query',
    'end_query',
    'load_model_response',
    'create_output_file',
]


def get_schema_file(filename: str):
    return open(f'{FOLDER}/schemas/{filename}', encoding='utf-8')


def query_interactive_args(
    opportunity_id: str | None,
    output_folder: str | None,
) -> tuple[str | None, str | None]:
    if opportunity_id is None:
        opportunity_id = input('Enter opportunity id (or nothing to skip): ').strip()
        if len(opportunity_id) == 0:
            opportunity_id = None
    if output_folder is None:
        output_folder = input('Enter output folder (or nothing to skip): ').strip()
        if len(output_folder) == 0:
            output_folder = None
    return opportunity_id, output_folder


def get_random_hash() -> str:
    from random import choice

    return choice(ascii_lowercase) + ''.join(choice(ascii_lowercase + digits) for _ in range(15))


def start_query(message: str, opportunity_id: str | None) -> tuple[str, datetime]:
    task = get_random_hash()
    logger.info(f'{message} (task=`%s`, id=`%s`)', task, opportunity_id)
    return task, datetime.now()


def end_query(message: str, start_time: datetime, task: str, opportunity_id: str | None) -> None:
    logger.info(
        f'{message}, elapsed time: %s (task=`%s`, id=`%s`)',
        datetime.now() - start_time,
        task,
        opportunity_id,
    )


def load_model_response(completion: Any, task: str, opportunity_id: str | None) -> Any:
    try:
        return json.loads(completion.choices[0].message.content)
    except json.JSONDecodeError:
        logger.error(
            'Recieved invalid JSON, when trying to load model response for opportunity (task=`%s`, id=`%s`)',
            task,
            opportunity_id,
        )
        return completion.choices[0].message.content


def create_query_file_contents(
    output: Any,
    opportunity_id: str | None,
) -> dict[str, Any]:
    return {
        'opportunity_id': opportunity_id,
        'output': output,
        'model': config.MODEL_NAME,
        'timestamp': str(datetime.now()),
    }


def create_output_file(
    contents: dict[str, Any],
    *,
    folder: str,
    task: str,
    opportunity_id: str | None = None,
) -> None:
    import os

    os.makedirs(folder, exist_ok=True)
    filename = f'{folder}/{datetime.now().strftime("%H-%M-%S")}-{task}.json'
    with open(filename, 'w') as f:
        json.dump(contents, f, indent=4)
    logger.info(
        'Written model response for opportunity to file `%s` (task=`%s`, id=`%s`)',
        filename,
        task,
        opportunity_id,
    )
