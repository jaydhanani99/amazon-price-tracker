# This is the docker file for nginx specifically

# Runs the nignx container un unprivileged mode for security reasons
FROM nginxinc/nginx-unprivileged:1-alpine

COPY ./default.conf /etc/nginx/conf.d/default.conf
COPY ./uwsgi_params /etc/nginx/uwsgi_params

# Temporarily switches to root user
USER root

RUN mkdir -p /vol/static
RUN chmod 755 /vol/static

USER nginx