.. You should enable this project on travis-ci.org and coveralls.io to make
   these badges work. The necessary Travis and Coverage config files have been
   generated for you.

.. image:: https://travis-ci.org/datopian/ckanext-noanonaccess.svg?branch=master
    :target: https://travis-ci.org/datopian/ckanext-noanonaccess

.. image:: https://coveralls.io/repos/datopian/ckanext-noanonaccess/badge.svg
  :target: https://coveralls.io/r/datopian/ckanext-noanonaccess

.. image:: https://pypip.in/download/ckanext-noanonaccess/badge.svg
    :target: https://pypi.python.org/pypi//ckanext-noanonaccess/
    :alt: Downloads

.. image:: https://pypip.in/version/ckanext-noanonaccess/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-noanonaccess/
    :alt: Latest Version

.. image:: https://pypip.in/py_versions/ckanext-noanonaccess/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-noanonaccess/
    :alt: Supported Python versions

.. image:: https://pypip.in/status/ckanext-noanonaccess/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-noanonaccess/
    :alt: Development Status

.. image:: https://pypip.in/license/ckanext-noanonaccess/badge.svg
    :target: https://pypi.python.org/pypi/ckanext-noanonaccess/
    :alt: License

=============
ckanext-noanonaccess
=============

Disable anonymous access to CKAN Classic frontend.

------------
Installation
------------

To install ckanext-noanonaccess:

1. Activate your CKAN virtual environment, for example::

     . /usr/lib/ckan/default/bin/activate

2. Install the ckanext-noanonaccess Python package into your virtual environment::

     pip install ckanext-noanonaccess

3. Add ``noanonaccess`` to the ``ckan.plugins`` setting in your CKAN
   config file (by default the config file is located at
   ``/etc/ckan/default/production.ini``).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu::

     sudo service apache2 reload


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

    nosetests --nologcapture --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.noanonaccess --cover-inclusive --cover-erase --cover-tests


---------------------------------
Registering ckanext-noanonaccess on PyPI
---------------------------------

ckanext-noanonaccess should be availabe on PyPI as
https://pypi.python.org/pypi/ckanext-noanonaccess. If that link doesn't work, then
you can register the project on PyPI for the first time by following these
steps:

1. Create a source distribution of the project::

     python setup.py sdist

2. Register the project::

     python setup.py register

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the first release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.1 then do::

       git tag 0.0.1
       git push --tags


----------------------------------------
Releasing a New Version of ckanext-noanonaccess
----------------------------------------

ckanext-noanonaccess is availabe on PyPI as https://pypi.python.org/pypi/ckanext-noanonaccess.
To publish a new version to PyPI follow these steps:

1. Update the version number in the ``setup.py`` file.
   See `PEP 440 <http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers>`_
   for how to choose version numbers.

2. Create a source distribution of the new version::

     python setup.py sdist

3. Upload the source distribution to PyPI::

     python setup.py sdist upload

4. Tag the new release of the project on GitHub with the version number from
   the ``setup.py`` file. For example if the version number in ``setup.py`` is
   0.0.2 then do::

       git tag 0.0.2
       git push --tags
