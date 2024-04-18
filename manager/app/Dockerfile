FROM python:3.9.2
WORKDIR /app
RUN apt update -y
RUN apt install supervisor logrotate -y
RUN apt install openvpn -y

COPY docker/supervisor/supervisord.conf /etc/supervisor

ADD logrotate.d/log.conf /etc/logrotate.d/log.conf

EXPOSE 5000