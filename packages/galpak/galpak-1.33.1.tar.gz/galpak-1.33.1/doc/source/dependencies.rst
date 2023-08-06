Dependencies
------------

The ``galpak`` module has been developed for Python ``>3`` and
 has been tested with Python ``3.5`` & ``3.7``

The following are **mandatory** python modules that ``galpak`` depends upon :

    - ``numpy>=1.14``
    - ``scipy``
    - ``astropy>=2.0``
    - ``matplotlib>=2.0``

``pyfits`` and ``asciitable`` are now obsolete since v1.8.7

The following are optional python modules that improves ``galpak`` performances :

    - ``pyfftw`` : https://pypi.python.org/pypi/pyFFTW
    - ``bottleneck`` : https://pypi.python.org/pypi/Bottleneck/

The following are optional python modules that improves ``galpak`` functionalities :

    - ``corner`` : https://pypi.python.org/pypi/corner
    - ``emcee`` : https://pypi.org/project/emcee/ (>3.0 in python>3.5)
    - ``pymultinest``: http://johannesbuchner.github.io/PyMultiNest/
    - ``mpdaf`` :  http://mpdaf.readthedocs.io/en/latest/


Development environment
-----------------------

This module also depends on ``unittest`` and ``nose`` for unit-testing.
The ``benchmark`` module is used in benchmarking.
The ``sphinx`` module is used to generate this documentation.
