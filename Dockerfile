# Use it with:
#  $ docker build -t wallapop-rss .
#  $ docker run -p5000:5000 wallapop-rss

FROM python:3

WORKDIR /

ADD src src

EXPOSE 5000

RUN pip3 install flask

CMD python3 src/wallapop-rss.py
