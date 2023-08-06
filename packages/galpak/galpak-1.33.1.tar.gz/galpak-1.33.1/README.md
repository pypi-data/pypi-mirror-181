WHAT IS IT
==========

GalPaK 3D is a tool to extract Galaxy Parameters and Kinematics from 3-Dimensional data,
using reverse deconvolution with Bayesian analysis Markov chain Monte Carlo. (random walk)

See the documentation for more details about the API on the [web site](http://galpak3d.univ-lyon1.fr/).


INSTALL
=======

pip install galpak

PYTHON DEPENDENCIES
-------------------


The galpak module has been developed for Python 2.7 and
    has been tested with Python 3.5 & 3.7

The following are mandatory python modules that galpak depends upon :

        numpy>=1.14
        scipy
        astropy>=2.0
        matplotlib>=2.0

The following optional python modules improve galpak performances :

        pyfftw : https://pypi.python.org/pypi/pyFFTW
        bottleneck : https://pypi.python.org/pypi/Bottleneck/

The following optional python modules improve galpak functionalities :

        corner : https://pypi.python.org/pypi/corner
        emcee : https://pypi.org/project/emcee/
        mpdaf : http://mpdaf.readthedocs.io/en/latest/


MPDAF PACKAGES
--------------

_Optional._

GalPaK provides a `MUSELineSpreadFunction` class that depends on `mpdaf.MUSE.LSF`.
Follow [MPDAF install instructions](https://mpdaf.readthedocs.io/en/latest/installation.html).

GalPaK also accepts MPDAF's Cubes as input.



I FOUND A BUG!
==============

THERE WILL BE BUGS. 
If you have found a bug in GalPaK3D please report it on the
galpak [forum/mailing list](https://groups.google.com/group/galpak3d).
Can _you_ reproduce it ? Provide the code and input cube(s).
You cannot reproduce it ? just describe what you're doing when it happens.

Also, we encourage everyone to give us feedback and participate in discussions.
We can use the [galpak3d](https://mail.python.org/mailman3/lists/galpak3d.python.org/) mailing list as well.

Email the above at <nicolas.bouche@univ-lyon1.fr> and/or add them as
test-case in the test suite.




HOW TO TEST
===========

untar and do
```
python -m pytest 
```


HOW TO DOCUMENT
===============

Install sphinx :
```
$ sudo apt-get install python-sphinx
```
or
```
$ pip install --user sphinx
```

Make your changes into the `doc/source` files.

Once its done, you can either :

    $ cd doc
    $ make html

or :

    $ doit doc


FITS Sanitizer
==============

`python fits_sanitizer.py [-h] [--prefix PREFIX] FILE [FILE ...]`

Sanitize specified FITS files. By default, this will overwrite the FITS files.
To create another file(s), you can specify a prefix using the --prefix option.

What this actually does :
    - Lowercase 'DEG' unit
    - that's all ! (it did some other things in the past)

positional arguments:
  FILE             A FITS file to sanitize

optional arguments:
  -h, --help       show this help message and exit
  --prefix PREFIX  A prefix to prepend to the filename(s), to create new files


Tip : you can sanitize a whole folder using the `*` wildcard : `python fits_sanitizer.py /myfits/*.fits`

Note that this will be superseded by the HyperspectralCube class `sanitize` method.


ACRONYMS
========

Real men never define acronyms. They understand them genetically.

FFT     Fast Fourier Transform
FITS    Flexible Image Transport System
FWHM    Full Width at Half Maximum
HDU     Header Data Unit
LSF     Line Spread Function
        Wavelength spread due to the dispersion of light in the atmosphere
MCMC    Markov Chain Monte Carlo
MPDAF   MUSE Python Data Analysis Framework
MUSE    Multi Unit Spectroscopic Explorer
NFM     Narrow Field Mode
PA      Position Angle
PC      ParseC
PSF     Point Spread Function
        Spatial spread caused by the atmosphere
SNR     Signal Noise Ratio
        The relative intensity of the signal from the noise
        Should be > 1, or the data is useless
WFM     Wide Field Mode
WSC     World Coordinates System


BLACKBOARD
==========

It would be smart to use a MCMC module :
    - [pymc3](https://docs.pymc.io/).


