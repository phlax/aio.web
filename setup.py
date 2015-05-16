"""
aio.web
"""
import sys
from setuptools import setup, find_packages

from aio.web import __version__ as version


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

setup(
    name='aio.web',
    version=version,
    description="Aio web server",
    classifiers=[
        "Programming Language :: Python 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='',
    author='Ryan Northey',
    author_email='ryan@3ca.org.uk',
    url='http://github.com/phlax/aio.web',
    license='GPL',
    packages=find_packages(),
    namespace_packages=['aio'],
    include_package_data=True,
    package_data={'': ['templates/*.html', 'README.rst']},
    test_suite="aio.app.tests",    
    zip_safe=False,
    tests_require=tests_require,
    install_requires=install_requires,
    entry_points={})
