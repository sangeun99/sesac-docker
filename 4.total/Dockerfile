FROM ubuntu:20.04

RUN apt update && \
    apt install nginx -y

COPY sesac /etc/nginx/sites-available/default


ENTRYPOINT ["nginx", "-g", "daemon off;"]