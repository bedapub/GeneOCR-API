FROM python:3.10-slim

WORKDIR /code

COPY ./app/requirements.txt /code/requirements.txt

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 libleptonica-dev tesseract-ocr libtesseract-dev python3-pil tesseract-ocr-eng tesseract-ocr-script-latn  -y

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

EXPOSE 8000

# Retrieve CA certificates and update the central CA location
ADD http://certinfo.roche.com/rootcerts/Roche%20Root%20CA%201.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/RocheEnterpriseCA1.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/RocheEnterpriseCA2.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/Roche%20Root%20CA%201%20-%20G2.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/Roche%20Enterprise%20CA%201%20-%20G2.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/Roche%20G3%20Root%20CA.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/Roche%20G3%20Issuing%20CA%201.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/Roche%20G3%20Issuing%20CA%202.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/Roche%20G3%20Issuing%20CA%203.crt /usr/local/share/ca-certificates/
ADD http://certinfo.roche.com/rootcerts/Roche%20G3%20Issuing%20CA%204.crt /usr/local/share/ca-certificates/
RUN update-ca-certificates --fresh

ENV REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt

RUN groupadd -g 1001 pmdagroup && \
    useradd -g pmdagroup -u 1001 pmdauser

USER pmdauser

WORKDIR /code/app

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

