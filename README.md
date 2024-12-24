# Shorturl-сервис

## Описание

Веб-сервис, для создания и хранения коротких ссылок, а так же перенаправления запросов по этим ссылкам на исходный ресурс.

API реализован на библиотеке FastAPI, хранение данных в SQLite.

## Как запустить

Все настройки приведены для запуска на локальной машине.
Если запустить с указанными здесь настройками, сервис будет доступен по адресу http://localhost:8000/

Документация и веб-интерфейс, предоставляемые фреймворком FastAPI доступны по адресу http://localhost:8000/docs

### Локально

1. Скопировать любым способом файлы проекта из каталога src
2. Установить зависимости из файла requirements.txt
```bash
pip install -r requirements.txt
```
3. Запустить веб сервер с приложением из каталога проекта src
```bash
uvicorn main:app --host 0.0.0.0 --port 80
```
### В Docker

#### Вариант 1. Собрать локальный образ

Собрать образ локально:
```bash
docker build -t shorturl-sqlite:latest .
```
Создать именованный том:
```bash
docker volume create shorturl_data
```
Запустить контейнер с томом:
```bash
docker run -d -p 8000:80 -v shorturl_data:/app/data shorturl-sqlite:latest
```

#### Вариант 2. Из образа, опубликованного на Docker hub

Образ опубликован на [Docker hub](https://hub.docker.com/repository/docker/alexanderanv/shorturl-sqlite)

Скачать образ:
```bash
docker pull alexanderanv/shorturl-sqlite:latest
```
Создать именованный том:
```bash
docker volume create shorturl_data
```

Запустить контейнер с томом:
```bash
docker run -d -p 8001:80 -v shorturl_data:/app/data alexanderanv/shorturl-sqlite:latest
```

