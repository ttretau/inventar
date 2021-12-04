FROM public.ecr.aws/bitnami/python:3.8

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

COPY . .
