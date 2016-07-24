import unittest

from needler.case import new_test_case


class NeedlerSuite(unittest.TestSuite):
    def __init__(self, baseline=False):
        super(NeedlerSuite, self).__init__()
        self.baseline = baseline

    @classmethod
    def from_config(cls, config):
        suite = cls(config.baseline)
        for case in config.cases:
            suite.addTest(new_test_case(config, case))
        return suite
