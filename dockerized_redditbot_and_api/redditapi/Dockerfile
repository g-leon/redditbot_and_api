FROM python:2.7.10

RUN pip install pymongo
RUN pip install flask
RUN pip install pyyaml

ADD api/ /redditapi/api/
ADD database/ /redditapi/database/

WORKDIR /redditapi

CMD python -m api/httpserver
