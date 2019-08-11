FROM ubuntu:16.04
#add module in dist-packages to python
ENV PYTHONPATH=/usr/lib/python{2.7,3,3.6}/dist-packages:$PYTHONPATH 
COPY [".", "/tmp"]
WORKDIR /tmp
RUN apt-get update -y && \
  apt-get install -y python-pip python-dev && \
  apt-get install -y python-nltk python-psycopg2 python-numpy python-scipy python-sklearn python-scrapy && \
  pip install flask
EXPOSE 80 
EXPOSE 5432
ENV FLASK_APP=flask_app/app.py
ENTRYPOINT ["bash"]
CMD ["./start.sh"]
