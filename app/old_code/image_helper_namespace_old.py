
"""
@image_helper_namespace.post(
    '/sharpen_slow',
    description='Sharpen image with tenserflow model',
    status_code=status.HTTP_200_OK,
    responses={
        **COMMON_API_RESPONSE_MODELS
    },
)
def image_sharpen_slow_endpoint(file: bytes = File(...)):
    image = preprocess_image(file)
    image = model_image(image)
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    res, im_png = cv2.imencode(".png", image)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")
"""