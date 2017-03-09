FROM python:3.6.0-alpine

MAINTAINER sopitz <simon.opitz@luminoso-consulting.de>

ADD bot/taigabot.py /

CMD python /taigabot.py
