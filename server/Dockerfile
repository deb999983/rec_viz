FROM python:3.9.7-alpine

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG INSTALL_DIR=/workspaces/server
ENV PYTHONPATH=$INSTALL_DIR
ENV INSTALL_DIR=$INSTALL_DIR

WORKDIR $INSTALL_DIR

COPY requirements.txt .

RUN \
 apk update && apk add bash && \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc python3-dev musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps


### Pull code
COPY . .

## Port expose
EXPOSE 8000

## Run entrypoint.sh
ENTRYPOINT ["./scripts/entrypoint.sh"]
# ENTRYPOINT ["sleep", "infinity"]
