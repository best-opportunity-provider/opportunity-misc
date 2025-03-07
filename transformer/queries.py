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
}

QUERY_MESSAGES = {
    'tags.system': (
        'You will be provided with HTML page of an opportunity, and your task is to parse '
        f'it according to this JSON schema: \n{SCHEMAS["tags"]}\nMake sure that you respond in English'
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
        temperature=0.3,
        # top_p=0.4,
        stream=False,
        extra_body={'nvext': {'guided_json': SCHEMAS['tags']}},
    )
    logger.info('Done querying tags for `%s`', opportunity_link)
    return completion
