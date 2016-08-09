from setuptools import find_packages, setup

setup(
    name='needler',
    version='0.1.0',
    description='Visually diff test case runner',
    long_description=open('README.rst').read(),
    author='Underdog.io Engineering',
    author_email='engineering@underdog.io',
    url='https://github.com/underdogio/needler',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    license='MIT',
    scripts=[
        'bin/needler',
    ],
)
