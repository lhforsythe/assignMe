FROM mysql:8.0.45-debian
WORKDIR /usr/src/assignmentOrganizer
COPY . .
RUN apt update && apt install python3-dev pkg-config python3-pip python3-django default-libmysqlclient-dev build-essential -y
RUN pip3 install mysqlclient requests django-allauth[socialaccount] --break-system-packages
EXPOSE 3306:3306
EXPOSE 8000:3307
