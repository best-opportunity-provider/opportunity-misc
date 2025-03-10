from openai import AsyncOpenAI

from . import config
from .config import (
    FOLDER,
    logger,
)


def get_schema_file(filename: str):
    return open(f'{FOLDER}/schemas/{filename}', encoding='utf-8')


SCHEMAS = {
    'tags': get_schema_file('categorized-tags.schema.json').read(),
    'form': get_schema_file('form.schema.json').read(),
    'general': get_schema_file('general.schema.json').read(),
    'selection': get_schema_file('selection.schema.json').read(),
    'details': get_schema_file('details.schema.json').read(),
}

QUERY_MESSAGES = {
    'tags.system': (
        'You will be provided with HTML page of an opportunity, and your task is to parse '
        f'it according to this JSON schema: {SCHEMAS["tags"]}.\n'
        "If you can't fill some fields from given HTML, you don't have to. "
        'Make sure that you respond in English.'
    ),
    'form.system': (
        'You will be provided with HTML page of an opportunity, and your task is to fill this JSON schema '
        f'arrocding to it: {SCHEMAS["form"]}.\nMake sure that you respond in English.'
    ),
    'general.system': (
        'You will be provided with HTML page of an opportunity, and your task is to fill this JSON schema '
        f'according to it: {SCHEMAS["general"]}.\nMake sure that you respond in English.'
    ),
    'selection.system': (
        'You will be provided with HTML page of an opportunity, and your task is to fill this JSON schema '
        f'according to it: {SCHEMAS["selection"]}.\nBase your answer only on provided HTML.'
    ),
    'details.system': (
        'You will be provided with HTML page of an opportunity, and your task is to fill this JSON schema '
        f'according to it: {SCHEMAS["details"]}.\nMake sure that you respond in English.'
    ),
}


async def query_opportunity_tags(client: AsyncOpenAI, opportunity_link: str, opportunity_page: str):
    logger.info('Querying tags for `%s`', opportunity_link)
    completion = await client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {'role': 'system', 'content': QUERY_MESSAGES['tags.system']},
            {'role': 'user', 'content': opportunity_page},
        ],
        temperature=0.25,
        top_p=0.4,
        stream=False,
        extra_body={'nvext': {'guided_json': SCHEMAS['tags']}},
    )
    logger.info('Done querying tags for `%s`', opportunity_link)
    return completion


async def query_opportunity_form(client: AsyncOpenAI, opportunity_link: str, opportunity_page: str):
    logger.info('Querying form for `%s`', opportunity_link)
    completion = await client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {'role': 'system', 'content': QUERY_MESSAGES['form.system']},
            {'role': 'user', 'content': opportunity_page},
        ],
        temperature=0.25,
        stream=False,
        extra_body={'nvext': {'guided_json': SCHEMAS['form']}},
    )
    logger.info('Done querying form for `%s`', opportunity_link)
    return completion


async def query_general_opportunity_info(
    client: AsyncOpenAI, opportunity_link: str, opportunity_page: str
):
    logger.info('Querying general info for `%s`', opportunity_link)
    completion = await client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {'role': 'system', 'content': QUERY_MESSAGES['general.system']},
            {'role': 'user', 'content': opportunity_page},
        ],
        temperature=0.25,
        stream=False,
        extra_body={'nvext': {'guided_json': SCHEMAS['general']}},
    )
    logger.info('Done querying general info for `%s`', opportunity_link)
    return completion


async def query_opportunity_selection_info(
    client: AsyncOpenAI, opportunity_link: str, opportunity_page: str
):
    logger.info('Querying selection info for `%s`', opportunity_link)
    completion = await client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {'role': 'system', 'content': QUERY_MESSAGES['selection.system']},
            {'role': 'user', 'content': opportunity_page},
        ],
        temperature=0.25,
        stream=False,
        extra_body={'nvext': {'guided_json': SCHEMAS['selection']}},
    )
    logger.info('Done querying selection info for `%s`', opportunity_link)
    return completion


async def query_opportunity_details_info(
    client: AsyncOpenAI, opportunity_link: str, opportunity_page: str
):
    logger.info('Querying details for `%s`', opportunity_link)
    completion = await client.chat.completions.create(
        model=config.MODEL_NAME,
        messages=[
            {'role': 'system', 'content': QUERY_MESSAGES['details.system']},
            {'role': 'user', 'content': opportunity_page},
        ],
        temperature=0.25,
        stream=False,
        extra_body={'nvext': {'guided_json': SCHEMAS['details']}},
    )
    logger.info('Done querying details for `%s`', opportunity_link)
    return completion
