# This file is placed in the Public Domain.
# pylint: disable=C0115,C0116


"irc"


import unittest


from genocide.irc import IRC


class TestIRC(unittest.TestCase):

    def test_irc(self):
        i = IRC()
        self.assertEqual(type(i), IRC)
