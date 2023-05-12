FROM python:3.8-slim-buster

WORKDIR /app

ADD . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn sqlalchemy pydantic requests dependency_injector

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
