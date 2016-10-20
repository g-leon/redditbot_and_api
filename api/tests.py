import unittest

import mock
from api.exceptions import BadRequestException
from api import httpserver

class TestApi(unittest.TestCase):

    subreddit = 'python'
    start = '12'
    end = '123'

    @mock.patch('api.httpserver._log')
    def test_validate_params(self, mock__log):

        # Missing 'subreddit' param
        self.assertRaises(
            BadRequestException,
            httpserver._validate_params,
            None, self.start, self.end,
        )

        # Missing 'from' parameter
        self.assertRaises(
            BadRequestException,
            httpserver._validate_params,
            self.subreddit, None, self.end,
        )

        # Missing 'to' parameter
        self.assertRaises(
            BadRequestException,
            httpserver._validate_params,
            self.subreddit, self.start, None,
        )

        # Invalid time interval
        self.assertRaises(
            BadRequestException,
            httpserver._validate_params,
            self.subreddit, self.end, self.start,
        )

    @mock.patch('api.httpserver._log')
    def test_normalize_params(self, mock__log):
        subreddit, start, end = httpserver._normalize_params(
            self.subreddit.upper(), self.start, self.end
        )
        self.assertEqual(subreddit, 'python')
        self.assertEqual(type(start), float)
        self.assertEqual(type(end), float)

        # Invalid integer values for time interval
        self.assertRaises(
            BadRequestException,
            httpserver._normalize_params,
            subreddit, '1A', '2b',
        )


if __name__ == '__main__':
    unittest.main()
