from setuptools import setup, find_packages

from codecs import open
from os import path 

HERE=path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="Elizabeth_SN",
    packages=find_packages(include=["Eli_SN_Version_Compare"]),
    version="1.1.0",
    long_description="Check if one version string is greater, lesser, or equal than other", 
    description="Makes a Version Comparison ",
    author="Elizabeth J Martinez A",
    license='MIT',
    include_package_data=True,
    install_requires=["numpy"],
    setup_requires=['pytest-runner'],
    tests_requires=['pytest==4.4.1'],
    test_suite='tests'
)   