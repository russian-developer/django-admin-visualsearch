from setuptools import setup, find_packages
from setuptools.command.test import test


class TestCommand(test):
    def run(self):
        from tests.runtests import runtests
        runtests()


setup(
    name='django-admin-visualsearch',
    version='1.2',
    description='Visualsearch.js for Django admin',
    long_description=open('README.md').read(),
    author='Constantin Slednev',
    author_email='c.slednev@gmail.com',
    license='BSD',
    url='https://github.com/unk2k/django-admin-visualsearch',
    packages=find_packages(),
    include_package_data=True,
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

