FROM python:3.11-slim
WORKDIR /usr/src/assignmentOrganizer
COPY . .
RUN apt update && apt install python3-dev pkg-config python3-pip python3-django default-libmysqlclient-dev build-essential nginx -y
RUN pip3 install mysqlclient requests django-allauth[socialaccount] gunicorn --break-system-packages
RUN cp webserver/nginx/assignMe /etc/nginx/sites-available/assignMe
RUN ln -s /etc/nginx/sites-available/assignMe /etc/nginx/sites-enabled
CMD ["sh", "-c", "nginx && cd djangoproject && gunicorn --bind 0.0.0.0:8000 --reload assignMe.wsgi"]