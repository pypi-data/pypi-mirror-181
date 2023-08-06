# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"rss"


import unittest


from genocide.rss import Fetcher


class TestRss(unittest.TestCase):

    def test_fetcher(self):
        fetcher = Fetcher()
        self.assertEqual(type(fetcher), Fetcher)
