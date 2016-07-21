import os
import unittest

from needle.cases import NeedleTestCase
from needle.driver import NeedlePhantomJS

HERE = os.path.abspath(os.path.dirname(__file__))
ONE_UP = os.path.dirname(HERE)
PHANTOMJS_PATH = os.path.join(ONE_UP, 'phantomjs/bin/phantomjs')


class Runner(object):
    def __init__(self, config):
        self.config = config

    def init_case(self, name, url, selector):
        case = TestCase(name, url, selector)
        case.cleanup_on_success = True
        case.save_baseline = self.config['baseline']
        case.baseline_directory = os.path.abspath(self.config['baseline_directory'])
        return case

    def suite(self):
        suite = unittest.TestSuite()
        for name, config in self.config['cases'].iteritems():
            case = self.init_case(name, config['url'], config['selector'])
            suite.addTest(case)
        return suite

    def run(self):
        return self.suite().run(TestResult())


class TestCase(NeedleTestCase):
    def __init__(self, name, url, selector):
        super(TestCase, self).__init__()
        self.name = name
        self.url = url
        self.selector = selector

    @classmethod
    def get_web_driver(cls):
        return NeedlePhantomJS(executable_path=PHANTOMJS_PATH)

    def runTest(self):
        self.driver.get(self.url)
        self.assertScreenshot(self.selector, self.name)


class TestResult(unittest.TestResult):
    def stopTestRun(self):
        super(TestResult, self).stopTestRun()
        print ''

    def addFailure(self, test, err):
        super(TestResult, self).addFailure(test, err)
        print 'f',

    def addSuccess(self, test):
        super(TestResult, self).addSuccess(test)
        print '.',
