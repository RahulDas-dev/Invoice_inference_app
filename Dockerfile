FROM python:3.11

RUN apt update && apt upgrade -y
RUN apt install -y poppler-utils

# Set the POPPLER_PATH environment variable dynamically
RUN POPPLER_PATH=$(dirname $(which pdftotext)) && echo "POPPLER_PATH=$POPPLER_PATH" >> /etc/environment
ENV POPPLER_PATH=$POPPLER_PATH
ENV PATH=$POPPLER_PATH:$PATH

COPY src /app/src
COPY run_app.py pyproject.toml uv.lock .env /app/
COPY .config.prod /app/.config

WORKDIR /app
RUN mkdir -p /app/temp

RUN pip install uv
RUN uv sync --frozen
RUN source .venv/bin/activate
ENTRYPOINT [ "sh", "-c", "gunicorn --bind \"${DIFY_BIND_ADDRESS:-0.0.0.0}:${DIFY_PORT:-5001}\" --workers ${SERVER_WORKER_AMOUNT:-1} --worker-class ${SERVER_WORKER_CLASS:-gevent} --worker-connections ${SERVER_WORKER_CONNECTIONS:-10} --timeout ${GUNICORN_TIMEOUT:-200} app:app" ]


