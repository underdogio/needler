import os
import platform
import setuptools
import shutil
import stat
import StringIO
import tarfile
import zipfile

import requests

PHANTOMJS_VERSION = '2.1.1'


def download_phantomjs():
    """Helper to download and install pre-built binary for PhantomJS"""
    url_template = 'https://bitbucket.org/ariya/phantomjs/downloads/{filename}.{ext}'
    filename_template = 'phantomjs-{version}-{system}'
    filename = None
    download_url = None

    system = platform.system()
    if system == 'Darwin':
        filename = filename_template.format(version=PHANTOMJS_VERSION, system='macosx')
        download_url = url_template.format(filename=filename, ext='zip')
    elif system == 'Linux':
        # `linux-x86_64` or `linux-i686`
        system_name = 'linux-{machine}'.format(machine=platform.machine())
        filename = filename_template.format(version=PHANTOMJS_VERSION, system=system_name)
        download_url = url_template.format(filename=filename, ext='tar.bz2')
    elif system == 'Windows':
        filename = filename_template.format(version=PHANTOMJS_VERSION, system='windows')
        download_url = url_template.format(filename=filename, ext='zip')

    resp = requests.get(download_url)
    resp.raise_for_status()
    if download_url.endswith('zip'):
        with zipfile.ZipFile(StringIO.StringIO(resp.content)) as archive:
            archive.extractall()
    else:
        with tarfile.TarFile.open(fileobj=StringIO.StringIO(resp.content)) as archive:
            archive.extractall()

    shutil.move(filename, 'phantomjs')
    os.chmod('phantomjs/bin/phantomjs', stat.S_IEXEC | stat.S_IREAD | stat.S_IWRITE)

# Check if local copy of PhantomJS exists or not
here = os.path.abspath(os.path.dirname(__file__))
phantomjs_dirname = os.path.join(here, 'phantomjs')
if not os.path.isdir(phantomjs_dirname):
    download_phantomjs()


setuptools.setup(
    name='needler',
    version='0.1.0',
    packages=setuptools.find_packages(),
    install_requires=open('requirements.txt').readlines(),
    scripts=[
        'bin/needler',
    ],
)
