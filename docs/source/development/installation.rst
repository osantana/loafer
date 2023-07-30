Development Installation
========================

Requirements
------------

* Poetry
* Python 3.10+


Development install
-------------------

After forking or checking out::

    $ cd loafer/
    $ poetry install
    $ poetry run pre-commit install


The requirements folder are only used for development, so we can easily
install/track dependencies required to run the tests using continuous
integration platforms.

Running tests::

    $ make test

Generating documentation::

    $ cd docs/
    $ make html


To configure AWS access, check `boto3 configuration`_ or export  (see `boto3 envvars`_)::

    $ export AWS_ACCESS_KEY_ID=<key>
    $ export AWS_SECRET_ACCESS_KEY=<secret>
    $ export AWS_DEFAULT_REGION=sa-east-1  # for example


.. _boto3 configuration: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
.. _boto3 envvars: http://boto3.readthedocs.org/en/latest/guide/configuration.html#environment-variable-configuration

Check the :doc:`../settings` section to see specific configurations.
