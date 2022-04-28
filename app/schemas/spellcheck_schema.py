from typing import Any, List
from pydantic import BaseModel, Field


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