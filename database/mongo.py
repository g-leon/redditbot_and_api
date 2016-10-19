import pymongo
import sys


class MongoDB(object):
    """
    Singleton class that wraps over Mongo database
    """
    _instance = None

    def __init__(self):
        if not self._instance:
           self._init()
        else:
            return self._instance

    def _init(self):
        self._instance = pymongo.MongoClient().reddit_bot['reddit']
        # Index for time range searches
        self._instance.create_index([
            ('subreddit', pymongo.ASCENDING),
            ('created_at', pymongo.DESCENDING),
        ])
        # Index for searches by keyword
        self._instance.create_index([
            ('content', pymongo.TEXT),
            ('title', pymongo.TEXT),
            ('subreddit', pymongo.ASCENDING),
            ('created_at', pymongo.DESCENDING),
        ])

    def insert_many(self, items=[]):
        if items:
            # 'ordered' flag is used with False for better performance
            self._instance.insert_many(items, ordered=False)

    def filter(self, subreddit, start, end, keyword=None):
        query = {
            'subreddit': subreddit,
            'created_at': {'$gte': start, '$lte': end},
        }
        if keyword:
            query['$text'] = {'$search': keyword}

        # For security reasons id is not returned
        items = []
        for i in self._instance.find(query, {'_id': False})\
                .sort('created_at', pymongo.DESCENDING):
            items.append(i)

        return items
