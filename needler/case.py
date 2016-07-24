from needle.cases import NeedleTestCase


def new_test_case(config, case_settings):
    test_cls = type(case_settings['name'], (NeedlerTestCase, ), dict(
        driver_class=config.driver_class,
        engine_class=config.engine_class,
        baseline_directory=config.baseline_directory,
        output_directory=config.output_directory,
        save_baseline=config.baseline,
        cleanup_on_success=True,
    ))
    return test_cls(**case_settings)


class NeedlerTestCase(NeedleTestCase):
    def __init__(self, name, url, selector, width=None, height=None):
        super(NeedleTestCase, self).__init__()
        self.name = name
        self.url = url
        self.selector = selector
        self.width = width
        self.height = height

    @classmethod
    def get_web_driver(cls):
        return cls.driver_class()

    def runTest(self):
        if self.width or self.height:
            self.set_viewport_size(width=self.width, height=self.height)

        self.driver.get(self.url)
        self.assertScreenshot(self.selector, self.name)
