from typing import Any

from openai import AsyncOpenAI

from .base import (
    get_schema_file,
    config,
    query_interactive_args,
    start_query,
    end_query,
    load_model_response,
    create_query_file_contents,
    create_output_file,
)


SCHEMA = get_schema_file('details.schema.json').read()
SYSTEM_MESSAGE = (
    'You will be provided with HTML page of an opportunity, and your task is to fill this JSON schema '
    f'according to it: {SCHEMA}.\nMake sure that you respond in English.'
)


async def query_opportunity_details(
    client: AsyncOpenAI,
    html: str,
    opportunity_id: str | None = None,
    output_folder: str | None = None,
    *,
    interactive: bool = False,
) -> Any:
    if interactive:
        opportunity_id, output_folder = query_interactive_args(opportunity_id, output_folder)
    task, start_time = start_query('Querying details for opportunity', opportunity_id)
    completion = await client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {'role': 'system', 'content': SYSTEM_MESSAGE},
            {'role': 'user', 'content': html},
        ],
        temperature=0.25,
        stream=False,
        extra_body={'nvext': {'guided_json': SCHEMA}},
    )
    end_query('Done querying details for opportunity', start_time, task, opportunity_id)
    response = load_model_response(completion, task=task, opportunity_id=opportunity_id)
    if output_folder is not None:
        create_output_file(
            create_query_file_contents(response, opportunity_id),
            folder=output_folder,
            task=task,
            opportunity_id=opportunity_id,
        )
    return response
