FROM python:3.7-alpine
MAINTAINER Jay Dhanani

ENV PATH="/scripts:${PATH}"

# Runs python in unbuffered environment
ENV PYTHONUNBUFFERED 1

# For installing the requirements
COPY ./requirements.txt /requirements.txt

# Here we required some packages to install our python requirements however we don't required to execute it further
# so we install it temporarily and give it name .tmp-build-deps and after installing python requirements we delete those packages
RUN apk add --update --no-cache --virtual .tmp-build-deps gcc libc-dev linux-headers musl-dev
# To install mysql on server
RUN apk add --update --no-cache mariadb-dev

# Installing the requirements
RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps


# Creating application directory in docker image
RUN mkdir /app
# Setting default working directory as app
WORKDIR /app
# Copying our app directory to docker app directory
COPY ./app /app


COPY ./scripts /scripts
RUN chmod +x /scripts/*

# To store the media file uploaded by user and we will serve this folder through nginx proxy
RUN mkdir -p /vol/web/media
# To store the static files of our project and we will serve this folder through nginx proxy
RUN mkdir -p /vol/web/static


# Adding user to docker container
RUN adduser -D user
# To assign /vol directory ownership to our user
RUN chown -R user:user /vol
# User has full access to web folder and everyone else has only read
RUN chmod -R 755 /vol/web
# Switching to user
USER user

# This is the entrypoint of our project in this file we will write some code to start the python uwsgi and server
CMD ["entrypoint.sh"]