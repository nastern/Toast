FROM ubuntu:18.04

LABEL maintainer="noahastern@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip
RUN pip3 install --upgrade pip

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app/

ENV LANG C.UTF-8

RUN pip3 install -r /app/requirements.txt

# Specific to deployment, not part of the code.
RUN pip3 install gunicorn

# So entrypoint does not run at root level
RUN groupadd app && useradd -g app app

RUN chown -R app:app ./

USER app

WORKDIR /app/flaskapp


CMD gunicorn --log-level=debug -b 0.0.0.0:5000 --workers=5 --timeout=60 app:app
