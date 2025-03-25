from typing import TypedDict


CONFIDENCE_THRESHOLD = 0.7


class Requirement(TypedDict):
    name: str
    confidence: float


class Benefit(TypedDict):
    name: str
    confidence: float


class TargetAudience(TypedDict):
    name: str
    confidence: float


class Salary(TypedDict):
    text: str
    confidence: float


class Expense(TypedDict):
    text: str
    confidence: float


class DetailsInput(TypedDict):
    requirements: list[Requirement]
    benefits: list[Benefit]
    target_audiences: list[TargetAudience]
    salary: Salary
    expenses: list[Expense]


class DetailsOutput(TypedDict):
    requirements: list[str]
    benefits: list[str]
    target_audiences: list[str]
    salary: str | None
    expenses: list[str]


async def translate_details(details: DetailsInput) -> DetailsOutput:
    return {
        'requirements': [
            requirement['name']
            for requirement in details['requirements']
            if requirement['confidence'] >= CONFIDENCE_THRESHOLD
        ],
        'benefits': [
            benefit['name']
            for benefit in details['benefits']
            if benefit['confidence'] >= CONFIDENCE_THRESHOLD
        ],
        'target_audiences': [
            audience['name']
            for audience in details['target_audiences']
            if audience['confidence'] >= CONFIDENCE_THRESHOLD
        ],
        'salary': (
            details['salary']['text']
            if details['salary']['confidence'] >= CONFIDENCE_THRESHOLD
            else None
        ),
        'expenses': [
            expense['text']
            for expense in details['expenses']
            if expense['confidence'] >= CONFIDENCE_THRESHOLD
        ],
    }
