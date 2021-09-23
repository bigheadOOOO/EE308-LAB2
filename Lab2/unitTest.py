# This is a unit testing file

import unittest
from codeForUnitTest import getResult

class GetResult(unittest.TestCase):
    def test_get_result(self):
        get_str = getResult(1)
        self.assertEqual(get_str, 35)

        get_str = getResult(2)
        self.assertEqual(get_str, [2, [3, 2]])

        get_str = getResult(3)
        self.assertEqual(get_str, 2)

        get_str = getResult(4)
        self.assertEqual(get_str, 2)