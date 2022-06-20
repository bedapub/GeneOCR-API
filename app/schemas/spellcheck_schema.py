from typing import Any, List
from pydantic import BaseModel, Field


class SpellCheckRequestModel(BaseModel):
    value: List[str] = Field(
        ...,
        description='Array of words that will be check for correct spelling'
    )
    type: str = Field(
        ...,
        description='Gene type for spell checking'
    )

class SpellCheckRequestModelAnalysis(BaseModel):
    value: List[str] = Field(
        ...,
        description='Array of words that will be check for correct spelling'
    )
    type: str = Field(
        ...,
        description='Gene type for spell checking'
    )
    input: List[str] = Field(
        ...,
        description='Analysis input'
    )

class SpellCheckModel(BaseModel):
    initial_word: str = Field(
        ...,
        desciption='Initial word'
    )
    gene_exists: bool = Field(
        ...,
        description='Does initial word exist in gene list'
    )
    suggestions: List[str] = Field(
        [],
        description='Suggestions for correct spelling of initial word'
    )
    best_canditate: str = Field(
        None,
        description='Best candidate for correct spelling'
    )

class SpellCheckModelAnalysis(BaseModel):
    initial_word: str = Field(
        ...,
        desciption='Initial word'
    )
    gene_exists: bool = Field(
        ...,
        description='Does initial word exist in gene list'
    )
    suggestions: List[str] = Field(
        [],
        description='Suggestions for correct spelling of initial word'
    )
    best_canditate: str = Field(
        None,
        description='Best candidate for correct spelling'
    )
    distance: float = Field(
        ...,
        description='Levenshtein distance'
    )
    is_correct: bool = Field(
        ...,
        description='Is gene correctly analyzed'
    )
    correct_in_candidates: bool = Field(
        None,
        description='Correct gene is in candidates list'
    )
