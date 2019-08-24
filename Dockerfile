FROM ubuntu:16.04
RUN apt-get update -y && \
  apt-get install -y nginx  && \
  apt-get install -y python-pip python-dev && \
  apt-get install -y python-nltk python-psycopg2 python-numpy python-scipy python-sklearn python-scrapy && \
  pip install flask && \
  apt-get install -y postgresql postgresql-contrib && \
  rm -rf /var/lib/apt/lists/*
RUN adduser --ingroup sudo --disabled-password --gecos '' stylometry
ENV PYTHONPATH=/usr/lib/python{2.7,3,3.6}/dist-packages:$PYTHONPATH 
COPY [".", "/tmp"]
COPY ["default","/etc/nginx/sites-available/default"]
WORKDIR /tmp
EXPOSE 80 
EXPOSE 5432
ENV FLASK_APP=flask_app/app.py
CMD ["bash","-c"]
