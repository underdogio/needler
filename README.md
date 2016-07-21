needler
=======

Needler is a visual diff test suite runner for [needle](https://github.com/bfirsh/needle).

By providing `needler` a YAML config defining the pages and components you wish to visually assert on.

**Note:** This project is still in development and not yet released, please use at your own risk.

## Installing

When installing `needler` will automatically try to download a prebuilt binary for [PhantomJS](http://phantomjs.org/).

```bash
git clone https://github.com/underdogio/needler
cd ./needler
python setup.py install
```

## CLI Interface

```bash
$ needler --help
usage: Needler [-h] [-c CONFIG] [-b] [-d BASELINE_DIRECTORY]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
  -b, --baseline
  -d BASELINE_DIRECTORY, --baseline-directory BASELINE_DIRECTORY
```

## Example

Given the following config file.
```yaml
# needler.yaml
cases:
  cnn_nav:
    url: 'http://www.cnn.com'
    selector: '#nav__plain-header'
```

```bash
# Collect the baseline images for testing
#   This will run all the cases and save the output images
#   to use as the baseline for assertions
needler --baseline

# Run the test cases and assert they are the
# same as the baseline images
needler
```
