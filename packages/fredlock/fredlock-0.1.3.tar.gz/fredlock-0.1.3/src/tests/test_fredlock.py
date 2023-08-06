"""
Unit Tests for fredlock
"""
import os
import unittest
from ddt import ddt, idata

from fredlock import fredlock

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

ACQ_PARAMS_DATA = {
    -2: dict(timeout=-1, blocking=True),
    -1: dict(timeout=-1, blocking=True),
    0: dict(blocking=False),
    1: dict(timeout=1, blocking=True),
    2: dict(timeout=2, blocking=True),
}


@ddt
class FredlockUnitTests(unittest.TestCase):
    """ Unit Tests for fredlock"""

    def setUp(self):
        """ Setup """

    @idata(ACQ_PARAMS_DATA.items())
    def test_acq_params(self, value):
        """ Check negative value results in correct  """
        timeout, expected = value
        self.assertDictEqual(fredlock.acq_params(timeout), expected)


if __name__ == '__main__':
    unittest.main()
