needler
=======

Needler is a visual diff test suite runner for `needle <https://github.com/bfirsh/needle>`__.

By providing ``needler`` a YAML config defining the pages and components you wish to visually assert on.

**Note:** This project is still in development and not yet released, please use at your own risk.

Installing
----------

.. code:: bash

    git clone https://github.com/underdogio/needler
    cd ./needler
    python setup.py install

Along with installing `needler` you will have to manually install any browser, or diffing software that you will need (e.g. `perceptualdiff <http://pdiff.sourceforge.net/>`__, `phantomjs <http://phantomjs.org/>`__, etc).

CLI Interface
-------------

.. code:: bash

    $ needler --help
    usage: Needler [-h] [-c CONFIG] [-b] [-d BASELINE_DIRECTORY]
                   [-o OUTPUT_DIRECTORY]

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -c CONFIG, --config CONFIG
      -b, --baseline
      -d BASELINE_DIRECTORY, --baseline-directory BASELINE_DIRECTORY
      -o OUTPUT_DIRECTORY, --output-directory OUTPUT_DIRECTORY
      -j, --json

Example
-------

Given the following config file.

.. code:: yaml

    # needler.yaml
    cases:
      homepage:
        url: 'http://localhost:5000/'
        components:
          content: '.content'
          header: '.header'
          footer: '.footer'

.. code:: bash

    # Collect the baseline images for testing
    #   This will run all the cases and save the output images
    #   to use as the baseline for assertions
    needler --baseline

    # Run the test cases and assert they are the
    # same as the baseline images
    needler

Config file
-----------

The `needler.yaml` config file is used to tell `needler` which test cases it should generate and how to run them.

.. code:: yaml

    # needler.yaml
    driver: firefox
    engine: perceptualdiff
    sizes:
      extra_large: 1440x809
      large: 1024x575
      medium: 768x1024
      small: 530x946
    cases:
      homepage:
        url: 'http://localhost:5000/'
        components:
          header: '.header'
          footer: '.footer'

The above example will tell `needler` to use the `firefox` driver, and the `perceptualdiff` command to test the image differences.

As well, it will generate 8 test cases, one for each case/component/size combination:

- `homepage_header_extra_large`
- `homepage_header_large`
- `homepage_header_medium`
- `homepage_header_small`.
- `homepage_footer_extra_large`
- `homepage_footer_large`
- `homepage_footer_medium`
- `homepage_footer_small`.
