from typing import List
from schemas.spellcheck_schema import SpellCheckModel, SpellCheckRequestModel
from fastapi.routing import APIRouter
from fastapi import status
from spellchecker import SpellChecker

wordspelling_check_namespace = APIRouter(prefix='/spelling')

spell = SpellChecker(language=None, case_sensitive=True)
spell.word_frequency.load_text_file('namespaces/dictionary.txt')

@wordspelling_check_namespace.post(
    '/suggestions',
    description='Get correct spelling of gene list',
    status_code=status.HTTP_200_OK,
)
def get_spelling_endpoint(input_value: SpellCheckRequestModel):
    result: List[SpellCheckModel] = []
    for gene in input_value.value:
        if not spell[gene]:
            candidates = spell.candidates(gene) 
            if len(candidates) == 1 and next(iter(candidates)) == gene:
                result.append(SpellCheckModel(initial_word=gene, gene_exists=False))
            else:
                correction = spell.correction(gene)
                result.append(SpellCheckModel(initial_word=gene, gene_exists=False, best_canditate=correction, suggestions=candidates))
        else:
            result.append(SpellCheckModel(initial_word=gene, gene_exists=True))
    return result


@wordspelling_check_namespace.get(
    '/check',
    description='Check if gene or other is valid',
    status_code=status.HTTP_200_OK,
)
def get_spelling_endpoint(word: str, type: str = 'gene'):
    return {
        "valid": bool(spell[word]),
        "initial_word": word
    }
