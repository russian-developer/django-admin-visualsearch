import visualsearch
from setuptools import setup, find_packages
from setuptools.command.test import test


class TestCommand(test):
    def run(self):
        from tests.runtests import runtests
        runtests()


setup(
    name='visualsearch',
    version=visualsearch.__version__,
    description='Visualsearch.js for Django admin',
    long_description=open('README.rst').read(),
    author='Constantin Slednev',
    author_email='c.slednev@gmail.com',
    license='BSD',
    url='https://github.com/ybw/visualsearch',
    platforms='any',
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Framework :: Django',
    ],
)

