from collections import OrderedDict
import json
import os
import sys
import traceback
import unittest

TERMINAL_WIDTH = 80
if 'COLUMNS' in os.environ:
    TERMINAL_WIDTH = int(os.environ['COLUMNS']) - 1


class NeedlerResults(unittest.TestResult):
    def __init__(self, config):
        super(NeedlerResults, self).__init__()
        self.config = config
        self.tests = OrderedDict()

    def addError(self, test, error):
        super(NeedlerResults, self).addError(test, error)
        self.tests[test.name]['error'] = error
        self.tests[test.name]['result'] = 'error'

    def addFailure(self, test, error):
        super(NeedlerResults, self).addFailure(test, error)
        self.tests[test.name]['error'] = error
        self.tests[test.name]['result'] = 'failure'

    def addSuccess(self, test):
        super(NeedlerResults, self).addSuccess(test)
        self.tests[test.name]['result'] = 'success'

    def startTest(self, test):
        super(NeedlerResults, self).startTest(test)
        self.tests[test.name] = OrderedDict(
            result='running',
            name=test.name,
            url=test.url,
            selector=test.selector,
            width=test.width,
            height=test.height,
            error=None,
            baseline_file=self.config.get_baseline_file(test.name),
            output_file=self.config.get_output_file(test.name),
            diff_file=self.config.get_diff_file(test.name),
        )
        self.print_status()

    def stopTest(self, test):
        super(NeedlerResults, self).stopTest(test)
        self.print_status()

    def stopTestRun(self):
        self.print_status()
        sys.stderr.write('\n')
        sys.stderr.flush()

    def print_status(self):
        line = '. '
        for test in self.tests.values():
            marker = '.'
            if test['result'] == 'error':
                marker = 'E'
            elif test['result'] == 'failure':
                marker = 'F'
            elif test['result'] == 'running':
                marker = 'R'
            line += marker
        sys.stderr.write(line + '\r')
        sys.stderr.flush()

    def print_results(self):
        if self.config.as_json:
            json.dump(self.tests, sys.stdout)
            sys.stdout.write('\n')
        else:
            for test_name, test in self.tests.items():
                # Skip successful tests
                if test['result'] == 'success':
                    continue

                sys.stdout.write('=' * TERMINAL_WIDTH + '\n')
                sys.stdout.write('{result} {test_name}\n'.format(result=test['result'].upper(), test_name=test_name))
                sys.stdout.write('=' * TERMINAL_WIDTH + '\n')
                for key, value in test.items():
                    if key == 'error':
                        continue
                    sys.stdout.write('{key}: {value}\n'.format(key=key, value=value))
                sys.stdout.write('-' * TERMINAL_WIDTH + '\n')
                _, message, tb = test['error']
                sys.stdout.write('{message}\n'.format(message=message))
                sys.stdout.write('-' * TERMINAL_WIDTH + '\n')
                traceback.print_tb(tb, file=sys.stdout)
                sys.stdout.flush()

            total = len(self.tests)
            success = len([t for t in self.tests.values() if t['result'] == 'success'])
            error = len([t for t in self.tests.values() if t['result'] == 'error'])
            failure = len([t for t in self.tests.values() if t['result'] == 'failure'])

            sys.stdout.write('=' * TERMINAL_WIDTH + '\n')
            sys.stdout.write('Results: total({total}) success({success}) failure({failure}) error({error})\n'
                             .format(total=total, success=success, failure=failure, error=error))
            sys.stdout.write('=' * TERMINAL_WIDTH + '\n')
        sys.stdout.flush()
