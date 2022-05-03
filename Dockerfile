FROM python:3.7-alpine
COPY ./requirements.txt requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# for security purpose
# create a separate user for development limits the scope of vulnerability
RUN adduser -D user
USER user
