FROM python:3.11-slim-buster

COPY poetry.lock pyproject.toml /tmp/
RUN pip install poetry && \
    cd /tmp && \
    poetry export -f requirements.txt --output requirements.txt && \
    pip install -r requirements.txt
