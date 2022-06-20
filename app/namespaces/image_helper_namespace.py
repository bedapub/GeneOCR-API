from fastapi.routing import APIRouter
from fastapi import status
from fastapi import File
import cv2
import numpy as np
import io
from config.api_configs import COMMON_API_RESPONSE_MODELS

from helpers.rotate import rotate_image

from helpers.image_sharpener import pil_fast_sharpener, cv2_kernel_fast_sharpener

image_helper_namespace = APIRouter(prefix='/image-helper')
from starlette.responses import StreamingResponse


@image_helper_namespace.post(
    '/rotate',
    description='Rotates image, so the text is horizontal aligned',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },
)
def image_rotation_endpoint(file: bytes = File(...)):
    img = cv2.imdecode(np.frombuffer(io.BytesIO(file).getbuffer(), np.uint8), -1)
    rotated = rotate_image(img)
    res, im_png = cv2.imencode(".png", rotated)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")


@image_helper_namespace.post(
    '/sharpen',
    description='Sharpen image with tenserflow model',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },
)
def image_sharpen_endpoint(file: bytes = File(...), algorythm: str = 'pil'):
    if algorythm == 'pil':
        image = pil_fast_sharpener(file)
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        res, im_png = cv2.imencode(".png", image)
        return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
    if algorythm == 'cv2kernel':
        img = cv2_kernel_fast_sharpener(file)
        res, im_png = cv2.imencode(".png", img)
        return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
    return 'Algorythm could not be found'


from schemas.spellcheck_schema import SpellCheckModelAnalysis, SpellCheckRequestModelAnalysis
from rapidfuzz.distance import Levenshtein
from statistics import mean, stdev
from scipy.stats import t
import numpy as np
from spellchecker import SpellChecker
from os import listdir
from os.path import isfile, join
from typing import List
import os
import pytesseract
from schemas.image_analyzation_schema import ImageAnalyzationResponseModel

files = [f for f in listdir('dictionary') if isfile(join('dictionary', f))]

spell_checker = {}

for file in files:
    spell = SpellChecker(language=None, case_sensitive=True)
    spell.word_frequency.load_text_file(f'dictionary/{file}')
    spell_checker[file.split('.')[0]] = spell

if os.name == 'nt':
    pytesseract.pytesseract.tesseract_cmd = pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract.exe'


@image_helper_namespace.post(
    '/analysis',
    description='Analyze text inside of image',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },
)
def image_analyzation_endpoint(file: bytes = File(...), organism: str = 'all', expected: str = ''):
    response_format: str = 'array'
    expected = expected.split()
    try:
        img = cv2.imdecode(np.frombuffer(io.BytesIO(file).getbuffer(), np.uint8), -1)
        h, w, c = img.shape
        if min((h, w)) < 300:
            scale_factor = float(350 / min((h, w))) * 1.5
            img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
        else:
            img = cv2.resize(img, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)
        try:
            img = rotate_image(img)
        except Exception as e:
            pass
        img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_AREA)
        kernel = np.array([[0, -1, 0],
                           [-1, 5, -1],
                           [0, -1, 0]])
        img = cv2.filter2D(src=img, ddepth=-1, kernel=kernel)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (5, 5), 0)
        text = pytesseract.image_to_string(img, lang='eng')
        if response_format == 'string':
            return ImageAnalyzationResponseModel(text=text, status="success", format="string")
        if response_format == 'array':
            split_text = text.split("\n")
            split_text = list(filter(lambda line: line.strip(), split_text))
            # return ImageAnalyzationResponseModel(text=split_text, status="success", format="array")

            input_for_spellcheck = SpellCheckRequestModelAnalysis(value=split_text, type=organism, input=expected)
            return get_spelling_endpoint(input_for_spellcheck)
        return ImageAnalyzationResponseModel(text=text, status="success", format="string")
    except Exception as e:
        print(e)
        return ImageAnalyzationResponseModel(status="failed", text=e, format=response_format)


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
        else:
            distance = distance / len(input_value.input[i])
        if not spell_checker[input_value.type][gene]:
            candidates = spell_checker[input_value.type].candidates(gene)
            if len(candidates) == 1 and next(iter(candidates)) == gene:
                result.append(SpellCheckModelAnalysis(initial_word=gene, gene_exists=False, distance=distance,
                                                      is_correct=is_correct))
            else:
                correction = spell_checker[input_value.type].correction(gene)
                correct_in_candidates = input_value.input[i] in correction
                result.append(SpellCheckModelAnalysis(initial_word=gene, gene_exists=False, best_canditate=correction,
                                                      suggestions=candidates, distance=distance, is_correct=is_correct,
                                                      correct_in_candidates=correct_in_candidates))
        else:
            result.append(
                SpellCheckModelAnalysis(initial_word=gene, gene_exists=True, distance=distance, is_correct=is_correct))

    invalid = len(list(filter(lambda item: item.is_correct == False, result)))
    list_len = len(result)
    coverage = 100 - ((100 / list_len) * invalid)
    distances = [float(item.distance) for item in result]
    distances = list(filter(lambda item: item != 0.0, distances))
    candidates = (list(filter(lambda item: item.correct_in_candidates is not None, result)))
    incorrect_candidates = (list(filter(lambda item: item.correct_in_candidates is False, candidates)))
    correct_candidates_coverage = 100 - ((100 / len(candidates)) * len(incorrect_candidates))
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
    dof = len(x) - 1
    t_crit = np.abs(t.ppf((1 - confidence) / 2, dof))
    return (m - s * t_crit / np.sqrt(len(x)), m + s * t_crit / np.sqrt(len(x)))
