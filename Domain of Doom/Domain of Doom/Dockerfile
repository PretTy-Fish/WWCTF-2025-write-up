FROM python:3.13.3-slim-bookworm

RUN apt-get update && apt-get install -y \
    netcat-traditional dnsutils \
    && rm -rf /var/lib/apt/lists/*

RUN pip install flask

WORKDIR /app

COPY ./code /app


RUN useradd -m web

# Root owns /app and files, only root can read/write/execute
RUN chown -R root:root /app \
    && chmod -R 700 /app

# Use root user to run the app (default user)
USER root

EXPOSE 5000

ENTRYPOINT ["python3", "app.py"]
