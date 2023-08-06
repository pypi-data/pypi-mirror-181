.. GalPaK documentation master file.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive, whatever that means. o.O

Welcome to GalPaK's documentation!
==================================

.. include:: common.rst

`GalPaK 3D <http://galpak3d.univ-lyon1.fr>`_ is a tool to extract Galaxy Parameters and Kinematics from 3-Dimensional data,
using reverse deconvolution with the Bayesian analysis procedure Markov Chain Monte Carlo.


.. figure:: images/deconvolution_example/GalPaK_cube_1101_from_paper_fig2.png
     :scale: 30%
     :align: center


Authors
-------

- Bouché N., Carfanta H., Schroetter I., Michel-Dansac L., Contini T., 2015, AJ `"GalPak3D:  A Bayesian parametric tool for extracting morpho-kinematics of galaxies from 3D data" <http://adsabs.harvard.edu/abs/2015AJ....150...92B>`_
- Full contact info can be found here: `contacts  <../authors.html>`_

.. include:: acknowledgments.rst

Do's and Don't
--------------
  The algorithm should never be used blindly and we stress that one should always
    (1) look at the chain using :meth:`plot_mcmc() <galpak.GalPaK3D.plot_mcmc>`,
    (2) look at the convergence of the parameters using :meth:`plot_geweke() <galpak.GalPaK3D.plot_geweke>`,
    (3) investigate possible covariance in the parameters using :meth:`plot_correlations() <galpak.GalPaK3D.plot_correlations>` and/or fix a parameter with the option  :ref:`known_parameters <fixed-value>`  to remove the degenerancy,
    (4) adjust the MCMC algorithm with the option :ref:`random_scale <random-scale>` (lower than 1 [default] for higher acceptance rate and vice versa) to ensure an acceptance rate of 30 to 50\%.
    or use the :meth:`autorun() <galpak.autorun>`.

Parameters description
----------------------

A description of the parameters meaning can be found `here <galaxy_parameters.html>`_


Table of Contents
-----------------

.. include:: table_of_contents.rst


Indices and tables
------------------

* :ref:`genindex`
* :ref:`search`
