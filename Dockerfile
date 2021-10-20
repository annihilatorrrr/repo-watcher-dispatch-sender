FROM python:3.10.0-slim-bullseye

# Don't use cached python packages
ENV PIP_NO_CACHE_DIR 1

# Make image lighter
RUN rm -rf /var/lib/apt/lists /var/cache/apt/archives /tmp

# Enter Workplace
WORKDIR /app/

# Copy folder
COPY . .

# Install dependencies
RUN pip3 install --upgrade pip

# Install poetry
RUN pip3 install --upgrade poetry==1.1.11

# Disable poetry virtualenv
RUN poetry config virtualenvs.create false

# Install requirements without dev requirements and without interaction
RUN poetry install --no-dev --no-interaction

# gives some issues with the docker image, so installing separately
RUN pip install platformdirs~=2.4.0

ENTRYPOINT ["poetry","run","python","src/main.py"]
