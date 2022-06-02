FROM python:3.9

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

WORKDIR /code/app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

