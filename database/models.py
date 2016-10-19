from pymongo.son_manipulator import SON


class Base(SON):
    def __init__(self, item, **kwargs):
        self['subreddit'] = kwargs.get('subreddit', '').lower()
        self['created_at'] = item.created_utc
        self['type'] = self.__class__.__name__.lower()


class Post(Base):
    def __init__(self, post):
        kwargs = {}
        kwargs['subreddit'] = post.subreddit.display_name
        super(Post, self).__init__(post, **kwargs)
        self['content'] = post.selftext
        self['title'] = post.title


class Comment(Base):
    def __init__(self, comment, **kwargs):
        super(Comment, self).__init__(comment, **kwargs)
        self['content'] = comment.body