A quick overview
================

.. include:: common.rst


The algorithm directly compares data-cubes with a disk parametric model
which has 9 or 10 free parameters [which can also be fixed independently].
The algorithm uses a Markov Chain Monte Carlo (MCMC) approach
with  non-traditional sampling laws in order to efficiently probe the parameter space.
More importantly, it uses the knowledge of the 3-dimensional spread-function
to return the intrinsic galaxy properties and the intrinsic data-cube.
The 3D spread-function class is flexible enough to handle any instrument.

One can use such an algorithm to constrain simultaneously the kinematics
and morphological parameters of (non-merging, i.e. regular) galaxies observed
in non optimal seeing conditions.
The algorithm can also be used on Adaptive-Optics (AO) data or on high-quality,
high-SNR data to look for non-axisymmetric structures in the residuals.


The algorithm can be (roughly) summarized as :

    #. Pick new random galaxy parameters using uniform priors [boundaries can be set]
    #. Create clean cube from parameters and convolve it with instrument's PSF+LSF
    #. Measure closeness of resulting convolved cube to input cube
    #. Accept/Reject galaxy parameters using Metropolis-Hasting algorithm
    #. Goto 1. until max iterations are reached
    #. Fill output attributes with data (chain, cubes, etc.)
    #. Compute and return best fit galaxy parameters from chain

.. warning::
  The output flux is in the pixel units, which may need to multiplied by CDELT3.

.. warning::
  The algorithm should never be used blindly and we stress that one should always
    (1) look at the convergence of the parameters using :meth:`plot_mcmc() <galpak.GalPaK3D.plot_mcmc>`,
    (2) investigate possible covariance in the parameters using :meth:`plot_correlations() <galpak.GalPaK3D.plot_correlations>` and/or fix a parameter with the option  :ref:`known_parameters <fixed-value>`  to remove the degenerancy,
    (3) adjust the MCMC algorithm with the option :ref:`random_scale <random-scale>` (lower than 1 [default] for higher acceptance rate and vice versa) to ensure an acceptance rate of 30 to 50\%.

Parameter meaning
-----------------

.. include:: galaxy_parameters.rst


Input Cubes supported
---------------------

* Any fits cube can be used provided that the z-axis represents wavelengths or frequencies.
* Any units are normally accepted as the algorithm works in velocity space (dlamba/lamba or dfrequency/frequency). Check the Instrument.z_step_kms value which is critial for the kinematic parameters.
* If the header  is incomplete (CRPIX3, CDELT3, CRVAL3, CUNIT3), the algorithm will try to use the default values assigned to the instrument. The user can specify these directly.
* If the header is complete, the instrument default pixel sizes will be over-written by the the information from the cube header.
* A `MPDAF <http://http://urania1.univ-lyon1.fr/mpdaf/>`_ ``Obj.Cube`` object is ok as input.
* To provide the variance, use a separate file with `variance' or via a MPDAF Obj.Cube. If no Variance is specified, the (edge of the) cube statistics will be used.
* In future versions, the variance can also be specified as a "STAT" or "VARIANCE" extension to the fits file

.. warning::
  Pay attention to the LSF FWHM, which should be specified in the same units as the cube.


Incomplete Header handling overview
-----------------------------------

.. figure:: images/GalPak_flow.png
     :scale: 40%
     :align: center

