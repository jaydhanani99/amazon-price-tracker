#!/bin/sh

# It means if any error occurse then exist the script with error code 0 do not run further commands
set -e

# This is the django management command which collect all the static files of our project and put then into static root
# The reason is during deployment djnago documentation suggests to use proxy like nginx or -
#   apache in order to serve the static files because proxy serves static file very effeciently compare to django applicaion itself.
python manage.py collectstatic --noinput

# Waiting for database service to start
echo Waiting for db service to start...;
while ! nc -z db 3306;
do
    sleep 1;
done;
echo Connected to db service!


python manage.py wait_for_db
python manage.py migrate
# Runs the uwsgi server
    # --socket specifies run as TCP socket on port 9000 from our proxy
    # master specifies to run as master service so it runs uwsgi in foreground instead of background
    # --enable-threads which specifies multi threading in uwsgi
    # last one is to specify wsgi.py file of our project
uwsgi --socket :9000 --master --enable-threads --module app.wsgi

