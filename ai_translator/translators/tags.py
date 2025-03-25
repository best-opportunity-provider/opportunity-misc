from typing import TypedDict
from enum import Enum

from .base import (
    logger,
)

CONFIDENCE_THRESHOLD = 0.7

# TODO: decide on final way to identify tag (string id or smth else)


class CategoryTag(Enum):
    INTERNSHIP = ('Internship', 'internship')
    JOB = ('Job', 'job')
    OTHER = ('Other', None)


CATEGORIES: dict[str, str | None] = {
    human_name: id for human_name, id in map(lambda x: x.value, CategoryTag)
}


class FormatTag(Enum):
    FULL_TIME = ('Full-time', 'full_time')
    PART_TIME = ('Part-time', 'part_time')
    IN_OFFICE = ('In office', 'in_office')
    REMOTE = ('Remote', 'remote')
    HYBRID = ('Hybrid', 'hybrid')


FORMAT_TAGS: dict[str, str] = {
    human_name: id for human_name, id in map(lambda x: x.value, FormatTag)
}


class IndustryTag(Enum):
    IT = ('IT', 'it')
    INDUSTRIAL_DESIGN = ('Industrial design', 'industrial_design')
    HOTEL_BUSINESS = ('Hotel business', 'hotel_business')
    MEDICINE = ('Medicine', 'medicine')


INDUSTRY_TAGS: dict[str, str] = {
    human_name: id for human_name, id in map(lambda x: x.value, IndustryTag)
}


class BranchTag(Enum):
    BACKEND = ('Backend', 'backend')
    FRONTEND = ('Frontend', 'frontend')
    USER_INTERFACE = ('User interface', 'user_interface')
    USER_EXPERIENCE = ('User experience', 'user_experience')


BRANCH_TAGS: dict[str, str] = {
    human_name: id for human_name, id in map(lambda x: x.value, BranchTag)
}


class Tag(TypedDict):
    name: str
    confidence: float


class TagGroup(TypedDict):
    standard: list[Tag]


class Tags(TypedDict):
    category: Tag
    format_tags: TagGroup
    industry_tags: TagGroup
    branch_tags: TagGroup


async def translate_tags(tags: Tags, opportunity_id: str) -> list[str]:
    result: list[str] = []
    if tags['category']['name'] in CATEGORIES:
        category = CATEGORIES[tags['category']['name']]
        if category is not None and tags['category']['confidence'] >= CONFIDENCE_THRESHOLD:
            result.append(category)
    else:
        logger.error(
            'Unexpected opportunity category `%s` (opportunity_id=`%s`)',
            tags['category']['name'],
            opportunity_id,
        )
    for prefix, dict in (
        ('format', FORMAT_TAGS),
        ('industry', INDUSTRY_TAGS),
        ('branch', BRANCH_TAGS),
    ):
        for tag in tags[f'{prefix}_tags']['standard']:
            if tag['name'] in dict:
                if tag['confidence'] >= CONFIDENCE_THRESHOLD:
                    result.append(dict[tag['name']])
            else:
                logger.error(
                    f'Unexpected opportunity {prefix} tag `%s` (opportunity_id=`%s`)',
                    tag['name'],
                    opportunity_id,
                )
    return result
