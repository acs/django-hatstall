import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-hatstall',
    version='0.1',
    packages=['hatstall'],
    include_package_data=True,
    license='GPLv3',
    description='A Django app to manage identities in Sorting Hat.',
    long_description=README,
    url='https://github.com/chaoss/grimoirelab-hatstall',
    author='Bitergia',
    author_email='acs@bitergia.com',
    keywords="development repositories analytics git github bugzilla jira jenkins",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Intended Audience :: Customer Service',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'django>=2.0',
    ]
)
