"""
aio.web
"""
import os
import sys
from setuptools import setup, find_packages

version = "0.0.8"

install_requires = [
    'setuptools',
    'aio.core',
    'aio.app',
    'aio.http',
    'aiohttp',
    'aiohttp_jinja2']

if sys.version_info < (3, 4):
    install_requires += [
        'asyncio']

tests_require = install_requires + ['aio.testing']


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = (
    'Detailed documentation\n'
    + '**********************\n'
    + '\n'
    + read("README.rst")
    + '\n')

setup(
    name='aio.web',
    version=version,
    description="Aio web server",
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='',
    author='Ryan Northey',
    author_email='ryan@3ca.org.uk',
    url='http://github.com/phlax/aio.web',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['templates/*.html', '*.rst']},
    test_suite="aio.app.tests",
    zip_safe=False,
    tests_require=tests_require,
    install_requires=install_requires,
    entry_points={})
