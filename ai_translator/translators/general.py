from typing import TypedDict

CONFIDENCE_THRESHOLD = 0.7


class Name(TypedDict):
    name: str
    confidence: float


class Provider(TypedDict):
    name: str
    confidence: float


class ShortDescription(TypedDict):
    description: str
    confidence: float


class InputInfo(TypedDict):
    name: Name
    provider: Provider
    short_description: ShortDescription


class OutputInfo(TypedDict):
    name: str | None
    provider: str | None
    short_description: str | None


async def translate_general_info(info: InputInfo) -> OutputInfo:
    return {
        'name': (
            info['name']['name'] if info['name']['confidence'] >= CONFIDENCE_THRESHOLD else None
        ),
        'provider': (
            info['provider']['name']
            if info['provider']['confidence'] >= CONFIDENCE_THRESHOLD
            else None
        ),
        'short_description': (
            info['short_description']['description']
            if info['short_description']['confidence'] >= CONFIDENCE_THRESHOLD
            else None
        ),
    }
