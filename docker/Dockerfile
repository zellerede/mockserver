FROM ubuntu:latest

WORKDIR /root
RUN  apt-get update
RUN  apt-get install -y python python-pip git
RUN  pip install django djangorestframework django-url-filter django-sslserver
RUN  git clone https://github.com/zellerede/mockserver.git

WORKDIR /root/mockserver
RUN  ./manage.py migrate
RUN  ./manage.py test
COPY runserver.sh .
RUN  chmod +x runserver.sh

EXPOSE 8000
EXPOSE 443

CMD  ./runserver.sh

# docker build -t mockserver:latest .
#
# - For HTTP:
# docker run -p 80:8000 -d mockserver
# curl localhost/__mock/
#
# - For HTTPS:
# docker run -p 443:443 -e HTTPS=True -d mockserver
# curl -k https://localhost/__mock/

