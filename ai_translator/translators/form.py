from typing import TypedDict
from enum import StrEnum


CONFIDENCE_THRESHOLD = 0.7


class FormFieldType(StrEnum):
    STRING = 'string'
    REGEX = 'regex'
    EMAIL = 'email'
    PHONE_NUMBER = 'phone_number'
    NUMBER = 'number'
    CHOICE = 'choice'
    COUNTRY = 'country'
    FILE = 'file'
    DATE = 'date'
    CHECKBOX = 'checkbox'


class FormInputFieldParameters(TypedDict):
    type: FormFieldType


class FormField(TypedDict):
    label: str
    is_required: bool
    parameters: FormInputFieldParameters


class FormInputField(FormField):
    confidence: float


class FormInput(TypedDict):
    fields: dict[str, FormInputField]
    confidence: float


async def translate_form(form: FormInput) -> dict[str, FormField] | None:
    if form['confidence'] < CONFIDENCE_THRESHOLD:
        return
    return {
        name: {key: value for key, value in field.items() if key != 'confidence'}
        for name, field in form['fields'].items()
        if field['confidence'] >= CONFIDENCE_THRESHOLD
    }
