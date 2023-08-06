Line Spread Functions
*********************


GalPaK provides two LSFs : **Gaussian** and **MUSE**.
These are used to extrude the 2D PSF image into 3D, right before its application in Fourier space.

You may use them as the ``lsf`` argument of the :class:`Instrument <galpak.Instrument>`,
as :ref:`described here <customizing-the-lsf>`.


Gaussian
--------

All instruments use this LSF model by default, with their own configuration :

.. autoclass:: galpak.GaussianLineSpreadFunction
    :members: as_vector


MUSE
----

This LSF requires the `mpdaf module <http://urania1.univ-lyon1.fr/mpdaf/chrome/site/DocCoreLib/index.html>`_,
specifically `mpdaf.MUSE.LSF <http://urania1.univ-lyon1.fr/mpdaf/chrome/site/DocCoreLib/user_manual_PSF.html>`_.

As this LSF is optional, you must explicitly tell your instrument to use it when you want to.

.. autoclass:: galpak.MUSELineSpreadFunction
    :members: as_vector


Interface
---------

In order to further customize the LSF you want to use,
you can :ref:`create your own LSF class <make-your-own-lsf>` and use it in the instrument,
it simply needs to implement the following interface :

.. autoclass:: galpak.LineSpreadFunction
    :members: as_vector
