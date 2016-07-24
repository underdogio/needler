import copy
import os

import yaml

from needle.driver import NeedleFirefox, NeedleChrome, NeedleIe, NeedleOpera, NeedleSafari, NeedlePhantomJS

CWD = os.getcwdu()
DEFAULT_OUTPUT = os.path.join(CWD, 'screenshots')
DEFAULT_BASELINE = os.path.join(DEFAULT_OUTPUT, 'baseline')
BROWSER_MAP = dict(
    firefox=NeedleFirefox,
    chrome=NeedleChrome,
    ie=NeedleIe,
    opera=NeedleOpera,
    safari=NeedleSafari,
    phantomjs=NeedlePhantomJS,
)


class NeedlerConfig(object):
    def __init__(self, config):
        self.config = config

    @classmethod
    def from_file(cls, filename):
        config = dict()
        # If they gave us a string, assume a filename
        if isinstance(filename, basestring):
            with open(filename, 'r') as fp:
                config = yaml.load(fp)
        else:
            config = yaml.load(filename)

        return cls(config)

    @property
    def baseline(self):
        return bool(self.config.get('baseline'))

    @baseline.setter
    def baseline(self, value):
        self.config['baseline'] = bool(value)

    @property
    def baseline_directory(self):
        return self.config.get('baseline_directory', DEFAULT_BASELINE)

    @baseline_directory.setter
    def baseline_directory(self, value):
        self.config['baseline_directory'] = value

    @property
    def output_directory(self):
        return self.config.get('output_directory', DEFAULT_OUTPUT)

    @output_directory.setter
    def output_directory(self, value):
        self.config['output_directory'] = value

    @property
    def driver(self):
        driver = self.config.get('driver')
        if not driver:
            driver = 'phantomjs'
        if isinstance(driver, basestring):
            driver = dict(name=driver)
        return driver

    @property
    def driver_class(self):
        return BROWSER_MAP.get(self.driver['name'])

    @property
    def engine_class(self):
        engine_name = self.config.get('engine', 'pil')
        if engine_name == 'percetualdiff':
            return 'needle.engines.perceptualdiff_engine.Engine'
        elif engine_name == 'imagemagick':
            return 'needle.engines.imagemagick_engine.Engine'
        else:
            # Default to `pil`
            return 'needle.engines.pil_engine.Engine'

    @property
    def sizes(self):
        if self.config.get('sizes'):
            for name, size in self.config['sizes'].iteritems():
                width, _, height = size.partition('x')
                yield dict(name=name, width=int(width), height=int(height))
        else:
            yield dict(name=None, width=None, height=None)

    @property
    def cases(self):
        cases = self.config.get('cases', dict())
        for size in self.sizes:
            for name, original_settings in cases.iteritems():
                # Make a copy since we might loop a few times and `dict`s are mutable
                settings = copy.deepcopy(original_settings)

                if 'selector' not in settings:
                    raise Exception('Expected test case "{name}" to have a "selector" property, none was found'
                                    .format(name=name))
                if 'url' not in settings:
                    raise Exception('Expected test case "{name}" to have a "url" property, none was found'
                                    .format(name=name))

                name = settings.get('name', name)
                if size['name']:
                    name = '{name}_{size}'.format(name=name, size=size['name'])
                settings['name'] = name
                settings['width'] = size['width']
                settings['height'] = size['height']
                yield settings
