import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'django-graphiter',
    version = '1.0',
    packages = ['graphiter'],
    package_data = {'graphiter': ['graphiter/templates/graphiter/*html'] },
    license = 'BSD License',
    description = 'Django app to store graphite chart URLs, combine them into pages, and adjust time frames via GET param.',
    long_description = README,
    url = 'https://github.com/jwineinger/django-graphiter',
    author = 'Jay Wineinger',
    author_email = 'jay.wineinger@gmail.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
