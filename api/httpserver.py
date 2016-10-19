from __future__ import with_statement

import logging
import os

import yaml
from flask import Flask, request, jsonify

from api.exceptions import BadRequestException
from database.mongo import MongoDB

_log = None
_config = None
_server = Flask('redditapi')
_db = None


@_server.route('/items', methods=['GET'])
def filter():
    subreddit = request.args.get("subreddit")
    start = request.args.get("from")
    end = request.args.get("to")
    keyword = request.args.get("keyword")

    subreddit, start, end = _normalize_params(subreddit, start, end)

    _validate_params(subreddit, start, end)

    try:
        items = _db.filter(subreddit, start, end, keyword)
    except:
        _log.error('Unable to query mongo', exc_info=True)
        raise BadRequestException(
            message='Internal server error',
            status_code=500,
        )

    return jsonify(items)


@_server.errorhandler(BadRequestException)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


def _validate_params(subreddit, start, end):
    """
    Checks that all parameters exist and
    that the time interval is correct
    """
    exc = None
    if subreddit is None:
        exc = BadRequestException(message="Missing 'subreddit' parameter")
    elif start is None:
        exc = BadRequestException(message="Missing 'from' parameter")
    elif end is None:
        exc = BadRequestException(message="Missing 'to' parameter")
    elif start > end:
        exc = BadRequestException(message='Time interval is invalid')

    if exc:
        _log.error(str(exc), exc_info=True)
        raise exc


def _normalize_params(subreddit, start, end):
    """
    Makes sure that 'subreddit' is low case
    and 'start' and 'end' are floats
    """
    try:
        subreddit = subreddit.lower()
        start = float(start)
        end = float(end)
    except:
        msg = 'Invalid parameters'
        _log.error(msg, exc_info=True)
        raise BadRequestException(msg)
    return subreddit, start, end


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
    _db = MongoDB()
    _server.run(host=_config.get('host', '0.0.0.0'),
                port=_config.get('port', 5000),
                debug=_config.get('debug', False))
