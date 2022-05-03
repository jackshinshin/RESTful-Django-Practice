FROM python:3.7-alpine
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN apk add --update --no-cache postgresql-client
# Installs temporary packages for required dependencies and deletes them after finishing dependencies installation
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps



RUN mkdir /app
WORKDIR /app
COPY ./app /app

# for security purpose
# create a separate user for development limits the scope of vulnerability
RUN adduser -D user
USER user
