from typing import List
from schemas.spellcheck_schema import SpellCheckModel, SpellCheckRequestModel, SpellCheckModelAnalysis, SpellCheckRequestModelAnalysis
from fastapi.routing import APIRouter
from fastapi import status
from spellchecker import SpellChecker
from os import listdir
from os.path import isfile, join
from rapidfuzz.distance import Levenshtein
from statistics import mean, stdev
from scipy.stats import t
import numpy as np

wordspelling_check_namespace = APIRouter(prefix='/spelling')

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

@wordspelling_check_namespace.post(
    '/suggestions-analysis',
    description='Get correct spelling of gene list',
    status_code=status.HTTP_200_OK,
)
def get_spelling_endpoint(input_value: SpellCheckRequestModelAnalysis):
    if len(input_value.input) != len(input_value.value):
        return {
            'message': 'expected and analyzed input, have different length'
        }
    result: List[SpellCheckModelAnalysis] = []
    for i, gene in enumerate(input_value.value):

        distance = Levenshtein.distance(gene, input_value.input[i])
        is_correct = False
        if distance == 0:
           is_correct = True
        if not spell_checker[input_value.type][gene]:
            candidates = spell_checker[input_value.type].candidates(gene)
            if len(candidates) == 1 and next(iter(candidates)) == gene:
                result.append(SpellCheckModelAnalysis(initial_word=gene, gene_exists=False, distance=distance, is_correct=is_correct))
            else:
                correction = spell_checker[input_value.type].correction(gene)
                correct_in_candidates = input_value.input[i] in correction
                print(correct_in_candidates)
                result.append(SpellCheckModelAnalysis(initial_word=gene, gene_exists=False, best_canditate=correction, suggestions=candidates, distance=distance, is_correct=is_correct, correct_in_candidates=correct_in_candidates))
        else:
            result.append(SpellCheckModelAnalysis(initial_word=gene, gene_exists=True, distance=distance, is_correct=is_correct))


    invalid = len(list(filter(lambda item: item.is_correct == False, result)))
    list_len = len(result)
    coverage = 100 - ((100 / list_len) * invalid)
    distances = [item.distance for item in result]
    print(calculate_confidence_interval(distances))
    candidates = (list(filter(lambda item: item.correct_in_candidates is not None, result)))
    incorrect_candidates = (list(filter(lambda item: item.correct_in_candidates is False, candidates)))
    correct_candidates_coverage = 100 - ((100 / len(candidates)) * len(incorrect_candidates))
    print(len(candidates), len(incorrect_candidates), correct_candidates_coverage)
    return {
        "result": result,
        "coverage": coverage,
        "Levenshtein_distance_mean": mean(distances),
        "Levenshtein_distance_stdev": stdev(distances),
        "Levenshtein_distance_confidence_interval": calculate_confidence_interval(distances),
        "correct_candidates_coverage": correct_candidates_coverage
    }

def calculate_confidence_interval(input_data, confidence=0.95):
    x = np.array(input_data)
    m = x.mean()
    s = x.std()
    dof = len(x)-1
    t_crit = np.abs(t.ppf((1-confidence)/2,dof))
    return (m-s*t_crit/np.sqrt(len(x)), m+s*t_crit/np.sqrt(len(x)))


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
    '/get-gene-organisms',
    description='Get a list of all possible gene organisms',
    status_code=status.HTTP_200_OK,
)
def get_all_gene_organisms():
    file_names = [file.split('.')[0] for file in files]
    return file_names
