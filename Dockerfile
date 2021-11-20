FROM python:3.10.0-slim-bullseye

# Don't use cached python packages
ENV PIP_NO_CACHE_DIR 1

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Enter Workplace
WORKDIR /app

# install dependencies
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y curl bash git \
    && apt-get autoremove --purge \
    && rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH="/root/.local/bin:$PATH"

# Do not create virtualenv
RUN poetry config virtualenvs.create false

# Copy package files
COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

# Install packages
RUN poetry install --no-dev --no-interaction --no-ansi && rm -rf /root/.cache

# Copy leftover files
COPY . .

# start the process
ENTRYPOINT poetry run python src/main.py
