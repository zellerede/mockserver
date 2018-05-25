FROM ubuntu:latest

WORKDIR /root
RUN  apt-get update
RUN  apt-get install -y python python-pip git
RUN  pip install django djangorestframework django-url-filter
RUN  git clone https://github.com/zellerede/mockserver.git

WORKDIR /root/mockserver
RUN  ./manage.py migrate
RUN  ./manage.py test

EXPOSE 8000

CMD  ./manage.py runserver 0.0.0.0:8000

# docker build -t mockserver:latest .
# docker run -p 8000:8000 -d mockserver:latest
#
