namesfr
=======

Random french name generator


Usage
-----

Namesfr can be used as a command line utility or imported as a Python package.

Command Line Usage
~~~~~~~~~~~~~~~~~~
To use the script from the command line:

.. code-block:: bash

    $ namesfr
    Alexandre Crouzier

Python Package Usage
~~~~~~~~~~~~~~~~~~~~
Here are examples of all current features:

.. code-block:: pycon

    >>> import namesfr
    >>> namesfr.get_full_name()
    u'Aurélien Germond'
    >>> namesfr.get_full_name(gender='male')
    u'Frédéric Castan'
    >>> namesfr.get_first_name()
    'Thierry'
    >>> namesfr.get_first_name(gender='female')
    'Iris'
    >>> namesfr.get_last_name()
    'Faust'


License
-------

This project is released under an `MIT License`_.

Data in the following files are public domain (governement data source 2018):

- dist.all.last
- dist.female.first
- dist.male.first

.. _mit license: http://th.mit-license.org/2013
