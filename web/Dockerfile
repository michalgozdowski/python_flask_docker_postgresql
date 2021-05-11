FROM python:3.6-alpine
WORKDIR app/
COPY app.py .
COPY requirements.txt .
RUN apk add postgresql-libs && \
    apk add --virtual .build-deps build-base gcc musl-dev postgresql-dev && \
    pip3 install -r requirements.txt && \
    apk del .build-deps
CMD ["python3", "app.py"]

