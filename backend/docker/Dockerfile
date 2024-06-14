FROM python:3.10.12

SHELL ["/bin/bash", "-c"]

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

# Установка GDAL и его зависимостей (для работы с координатами)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gdal-bin \
        libgdal-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* # Очистка кеша для уменьшения размера образа

RUN pip install --upgrade pip

WORKDIR /backend

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY . .
COPY ./docker/assets/fonts/MyriadPro-Bold.ttf /usr/local/share/fonts/MyriadPro-Bold.ttf
COPY ./docker/assets/fonts/MyriadPro-Regular.ttf /usr/local/share/fonts/MyriadPro-Regular.ttf


RUN ["chmod", "+x", "./docker/run.sh"]