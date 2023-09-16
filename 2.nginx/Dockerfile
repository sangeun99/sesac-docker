FROM ubuntu:20.04

RUN apt update && \
    apt install nginx -y && \
    apt install curl -y && \
    apt install vim -y

WORKDIR /var/www/html

COPY . .

ENTRYPOINT ["nginx", "-g", "daemon off;"]
