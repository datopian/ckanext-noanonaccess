[![Tests](https://github.com/datopian/ckanext-noanonaccess/actions/workflows/test.yml/badge.svg)](https://github.com/datopian/ckanext-noanonaccess/actions/workflows/test.yml) [![CKAN](https://img.shields.io/badge/ckan-2.10.x-blue.svg)]() [![CKAN](https://img.shields.io/badge/ckan-2.9.x-blue.svg)]()

ckanext-noanonaccess
=============

Disable anonymous access to the CKAN classic frontend. This extension redirects anonymous users to the login page and only allow if they are logged in. It's useful if you're using CKAN as an internal data management system or have  a decoupled frontend for the end users.



------------
Installation
------------

To install ckanext-noanonaccess:

1. Activate your CKAN virtual environment, for example::

        . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-noanonaccess Python package into your virtual environment::

        pip install ckanext-noanonaccess

3. Add ``noanonaccess`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at;)

        /etc/ckan/default/production.ini

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

        sudo service apache2 reload

--------------------
Configuration Options
--------------------
You can also specify allowed page URLs in blueprints by using either the blueprint's name or path URL in regex format, separated by spaces.

    ckanext.noanonaccess.allowed_blueprint = feeds.general feeds.group
    ckanext.noanonaccess.allowed_paths = /about/.* /oauth2/callback

------------------------
Development Installation
------------------------

To install ckanext-noanonaccess for development, activate your CKAN virtualenv and
do::

    git clone https://github.com/datopian/ckanext-noanonaccess.git
    cd ckanext-noanonaccess
    python setup.py develop
    pip install -r dev-requirements.txt


-----------------
Running the Tests
-----------------

To run the tests, do::

    pytest --ckan-ini=test.ini 

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    pytest --ckan-ini=test.ini --cov=ckanext.noanonaccess --disable-warnings ckanext/noanonaccess/tests
