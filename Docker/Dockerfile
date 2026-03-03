FROM mysql:8.0.45-debian
WORKDIR /usr/src/assignmentOrganizer
COPY . .
RUN apt update && apt install python3 python3-pip -y
RUN pip3 install mysql-connector requests Django --break-system-packages
EXPOSE 3306:3306
EXPOSE 8000:3307
