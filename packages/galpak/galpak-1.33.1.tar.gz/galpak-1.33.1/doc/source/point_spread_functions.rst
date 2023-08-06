Point Spread Functions
**********************


GalPaK provides the two most common PSF : **Gaussian** and **Moffat**.

You may use them as the ``psf`` argument of the Instrument, as :ref:`described here <customizing-the-psf>`.


Gaussian
--------

All instruments use this PSF model by default, with their own configuration :

.. autoclass:: galpak.GaussianPointSpreadFunction
    :members: as_image


Moffat
------

.. autoclass:: galpak.MoffatPointSpreadFunction
    :members: as_image


Interface
---------

In order to furthermore customize the PSF you want to use,
you can :ref:`create your own PSF class <make-your-own-psf>` and use it in the instrument,
it simply needs to implement the following interface :

.. autoclass:: galpak.PointSpreadFunction
    :members: as_image