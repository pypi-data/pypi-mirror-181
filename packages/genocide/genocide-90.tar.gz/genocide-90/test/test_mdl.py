# This file is placed in the Public Domain.
# pylint: disable=E1101,C0115,C0116,E0611


"model"


import unittest


from genocide.model import oorzaak
from genocide.object import Object


class TestModel(unittest.TestCase):

    def test_model(self):
        self.assertEqual(type(oorzaak), Object)
