import unittest


class NeedlerResults(unittest.TestResult):
    @classmethod
    def from_config(cls, config):
        return cls()

    def addError(self, test, error):
        super(NeedlerResults, self).addError(test, error)
        print error

    def addFailure(self, test, error):
        super(NeedlerResults, self).addFailure(test, error)
        print error

    def addSuccess(self, test):
        super(NeedlerResults, self).addSuccess(test)
        print 'SUCCESS'

    def startTest(self, test):
        super(NeedlerResults, self).startTest(test)
        print 'Running test case: {name}'.format(name=test.name)

    def print_results(self):
        print ('Finished running tests: ran({ran}) errors({errors}) failures({failures})'
               .format(ran=self.testsRun, errors=len(self.errors), failures=len(self.failures)))
