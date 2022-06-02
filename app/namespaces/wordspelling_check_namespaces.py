from typing import List
from schemas.spellcheck_schema import SpellCheckModel, SpellCheckRequestModel
from fastapi.routing import APIRouter
from fastapi import status
from spellchecker import SpellChecker
from os import listdir
from os.path import isfile, join

wordspelling_check_namespace = APIRouter(prefix='/spelling')

spell = SpellChecker(language=None, case_sensitive=True)
spell.word_frequency.load_text_file('namespaces/dictionary.txt')

files = [f for f in listdir('dictionary') if isfile(join('dictionary', f))]

spell_checker = {}

for file in files:
    spell = SpellChecker(language=None, case_sensitive=True)
    spell.word_frequency.load_text_file(f'dictionary/{file}')
    spell_checker[file.split('.')[0]] = spell

@wordspelling_check_namespace.post(
    '/suggestions',
    description='Get correct spelling of gene list',
    status_code=status.HTTP_200_OK,
)
def get_spelling_endpoint(input_value: SpellCheckRequestModel):
    result: List[SpellCheckModel] = []
    for gene in input_value.value:
        if not spell_checker[input_value.type][gene]:
            candidates = spell_checker[input_value.type].candidates(gene)
            if len(candidates) == 1 and next(iter(candidates)) == gene:
                result.append(SpellCheckModel(initial_word=gene, gene_exists=False))
            else:
                correction = spell_checker[input_value.type].correction(gene)
                result.append(SpellCheckModel(initial_word=gene, gene_exists=False, best_canditate=correction, suggestions=candidates))
        else:
            result.append(SpellCheckModel(initial_word=gene, gene_exists=True))
    return result


@wordspelling_check_namespace.get(
    '/check',
    description='Check if gene or other is valid',
    status_code=status.HTTP_200_OK,
)
def get_spelling_endpoint(word: str, type: str):
    return {
        "valid": bool(spell_checker[type][word]),
        "initial_word": word
    }


@wordspelling_check_namespace.get(
    '/get-gene-types',
    description='Get a list of all possible gene types',
    status_code=status.HTTP_200_OK,
)
def get_all_gene_types():
    file_names = [file.split('.')[0] for file in files]
    return file_names
