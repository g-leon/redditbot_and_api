FROM python:2.7.10

RUN pip install praw
RUN pip install pymongo
RUN pip install pyyaml

ADD bot/ /redditbot/bot/
ADD database/ /redditbot/database/

WORKDIR /redditbot

CMD python -m bot/reddit