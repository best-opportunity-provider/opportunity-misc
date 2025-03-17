import asyncio
from typing import Any

from openai import AsyncOpenAI

from .base import (
    query_interactive_args,
    start_query,
    end_query,
    create_query_file_contents,
    create_output_file,
)
from .details import query_opportunity_details
from .form import query_opportunity_form
from .general import query_opportunity_general_info
from .selection import query_opportunity_selection_info
from .tags import query_opportunity_tags


__all__ = [
    'query_opportunity_details',
    'query_opportunity_form',
    'query_opportunity_general_info',
    'query_opportunity_selection_info',
    'query_opportunity_tags',
    'query_opportunity',
]


async def query_opportunity(
    client: AsyncOpenAI,
    html: str,
    form_html: str | None = None,
    opportunity_id: str | None = None,
    output_folder: str | None = None,
    *,
    interactive: bool = False,
) -> dict[str, Any]:
    if interactive:
        opportunity_id, output_folder = query_interactive_args(opportunity_id, output_folder)
    if form_html is None:
        form_html = html
    task, start_time = start_query('Querying information about opportunity', opportunity_id)
    async with asyncio.TaskGroup() as tg:
        tags = tg.create_task(query_opportunity_tags(client, html, opportunity_id))
        form = tg.create_task(query_opportunity_form(client, form_html, opportunity_id))
        general = tg.create_task(query_opportunity_general_info(client, html, opportunity_id))
        selection = tg.create_task(query_opportunity_selection_info(client, html, opportunity_id))
        details = tg.create_task(query_opportunity_details(client, html, opportunity_id))
    end_query('Done querying information about opportunity', start_time, task, opportunity_id)
    output = {
        'tags': tags.result(),
        'form': form.result(),
        'general': general.result(),
        'selection': selection.result(),
        'details': details.result(),
    }
    if output_folder is not None:
        create_output_file(
            create_query_file_contents(output, opportunity_id),
            folder=output_folder,
            task=task,
            opportunity_id=opportunity_id,
        )
    return output
