import logging
import yaml
import praw
import time
import os

from database.models import Post, Comment
from database.mongo import MongoDB

_log = None
_config = None
_reddit_client = None
_mongo = None

def main():
    # Remember the last post for each subreddit
    # in order to not retrieve the same posts again
    last_post = {}

    subreddits = _config.get('subreddits', [])

    while True:
        for sr in subreddits:
            subreddit = _reddit_client.get_subreddit(sr)

            # Get latests posts for this subreddit
            post_models = []
            for post in subreddit.get_new(
                    limit=_config.get('posts-limit', 1),
                    params={"before": last_post.get(sr)}
            ):
                post_models.append(Post(post))

                # Get comments associated with this post
                comment_models = []
                post.replace_more_comments(limit=16, threshold=10)
                for comment in praw.helpers.flatten_tree(post.comments):
                    comment_models.append(Comment(comment, subreddit=sr))

                # Insert comments
                try:
                    _mongo.insert_many(comment_models)
                except:
                    _log.error('Unable to insert comments', exc_info=True)

                # Remember last post to not fetch it again
                last_post[sr] = post.fullname

            # Insert post
            try:
                _mongo.insert_many(post_models)
            except:
                _log.error('Unable to insert posts', exc_info=True)

        # Request limiter
        time.sleep(_config.get('rate-limit', 1))


def _load_config():
    location = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    location = str(location)
    try:
        with open(location + '/config.yml', 'r') as yamlfile:
            cfg = yaml.load(yamlfile)
    except EnvironmentError:
        _log.critical("Can't find config file", exc_info=True)
        raise
    return cfg


def _init_logger():
    log = logging.getLogger(__file__)
    log.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    log.addHandler(handler)
    return log


if __name__ == '__main__':
    _log = _init_logger()
    _config = _load_config()
    _mongo = MongoDB()
    _reddit_client = praw.Reddit(
        user_agent="My cool reddit script",
        log_requests=_config.get('log-requests', False),
    )

    try:
        _log.info('Starting redditbot...')
        main()
    except KeyboardInterrupt:
        _log.info("redditbot is shutting down...")

    _log.info('reddibot is done.')
