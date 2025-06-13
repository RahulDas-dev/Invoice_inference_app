FROM python:3.11

RUN apt update && apt upgrade -y
RUN apt install -y poppler-utils

# Set the POPPLER_PATH environment variable dynamically
RUN POPPLER_PATH=$(dirname $(which pdftotext)) && echo "POPPLER_PATH=$POPPLER_PATH" >> /etc/environment
ENV POPPLER_PATH=$POPPLER_PATH
ENV PATH=$POPPLER_PATH:$PATH

# copy the application to app directory 
COPY src /app/src
COPY run_app.py /app/run_app.py
COPY pyproject.toml /app/pyproject.toml
COPY uv.lock /app/uv.lock
COPY .env /app/.env
COPY .config.prod /app/.config

# app directory is the current working directory
WORKDIR /app

# create a temp direcoroty
RUN mkdir -p /app/temp

# install uv
RUN pip install --no-cache-dir uv==0.4.24

# install dependency
RUN uv sync --frozen --no-dev

# run the app
ENTRYPOINT [ "uv", "run", "hypercorn", "run_app:app", "--bind", "0.0.0.0:5005" ]


