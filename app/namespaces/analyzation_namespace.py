
from fastapi.routing import APIRouter
from fastapi import status
from PIL import Image
import pytesseract
from fastapi import FastAPI, File, UploadFile
import io

from config.api_configs import COMMON_API_RESPONSE_MODELS
from schemas.image_analyzation_schema import ImageAnalyzationRequestModel, ImageAnalyzationResponseModel

analyzation_namespace = APIRouter(prefix='/analyze')

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\geserp\Anaconda3\Library\bin\tesseract.exe'

@analyzation_namespace.post(
    '/image',
    description='Analyze text inside of image',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },

)
def image_analyzation_endpoint(file: bytes = File(...)):
    try:
        image = Image.open(io.BytesIO(file))
        text = pytesseract.image_to_string(image, lang='eng')
        return ImageAnalyzationResponseModel(text=text, status="success")
    except Exception as e:
        return ImageAnalyzationResponseModel(status="failed", text=e)