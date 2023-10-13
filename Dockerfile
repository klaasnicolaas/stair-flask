# Build the static files
FROM node:20 as builder

WORKDIR /app

COPY ./app/static/package.json ./app/static/package-lock.json /app/static/
RUN cd /app/static && npm install

COPY ./app/static /app/static
RUN cd /app/static && npm run build

# Build the Flask application
FROM python:3.11-alpine

RUN apk update && apk add \
    python3-dev \
    gcc \
    libc-dev \
    libffi-dev

WORKDIR /app

COPY pyproject.toml poetry.lock /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app
COPY --from=builder /app/static /app/static

CMD ["poetry", "run", "python", "run.py"]
# CMD ["poetry", "run", "uwsgi", "--ini", "uwsgi.ini"]
