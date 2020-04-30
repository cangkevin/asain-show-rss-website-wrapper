FROM python:3.6-alpine

ARG BASE_URL
ARG ELASTICSEARCH_URL

RUN adduser -D seashows

WORKDIR /app

COPY --chown=seashows:seashows requirements.txt .
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY --chown=seashows:seashows website website
COPY --chown=seashows:seashows seashows.py config.py startup.sh ./
RUN chmod +x startup.sh

ENV FLASK_APP seashows.py
ENV ELASTICSEARCH_URL $ELASTICSEARCH_URL
ENV BASE_URL $BASE_URL

USER seashows

EXPOSE 5000
ENTRYPOINT ["./startup.sh"]
