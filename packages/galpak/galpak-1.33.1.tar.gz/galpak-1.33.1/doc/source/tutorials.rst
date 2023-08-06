Tutorials Level 0
*****************

.. include:: common.rst


Preparing the input cube
------------------------

Make sure your cube :

- is written as a fits file
- has a third dimension representing wavelengths or frequencies.
- has a minimum info in the header.
    - The header should have units but the algorithm works in velocity space (dlamba/lamba or dfrequency/frequency). Check the Instrument.z_step_kms value which is critial for the kinematic parameters.
    - If the header  is incomplete (CRPIX3, CDELT3, CRVAL3, CUNIT3), the algorithm will try to use the default values assigned to the instrument. The user can specify these directly.
- is adequately cropped in x and y and along z around the galaxy (performance goes as Npix log(Npix)!)
- is continuum subtracted (!) as the algorithm does not fit the continuum
- best to provide the variance in a separate file or via a `MPDAF <http://http://urania1.univ-lyon1.fr/mpdaf/>`_ ``Obj.Cube``. If no variance is specified, the cube statistics will be used.

.. warning::
    You should specify the PSF and spectral LSF that are in effect for your cube. Don't trust the defaults.

.. note::
    For MPDAF users, a `MPDAF <http://http://urania1.univ-lyon1.fr/mpdaf/>`_ ``Obj.Cube`` object is ok as input.

Test GalpaK with MUSE per default
---------------------------------


The simplest way to use GalPaK is as follows : ::

        import galpak
        from galpak import DefaultModel, ModelSersic
        gk = galpak.run('GalPaK_cube_1101_from_paper.fits', instrument=galpak.MUSEWFM(psf_fwhm=1.0), model=DefaultModel(rotation_curve='arctan') )

or if you want to auto-tune the random_scale parameter: ::

        import galpak
        from galpak import DefaultModel, ModelSersic
        gk = galpak.autorun('GalPaK_cube_1101_from_paper.fits',  instrument=galpak.MUSEWFM(psf_fwhm=1.0), model=DefaultModel(rotation_curve='arctan'))

Using seeing as short for PSF FWHM: ::

        import galpak
        from galpak import DefaultModel, ModelSersic
        gk = galpak.GalPaK3D('GalPaK_cube_1101_from_paper.fits', seeing=1.0, instrument=galpak.MUSEWFM())
        gk.run_mcmc(model=DefaultModel(rotation_curve='arctan')

.. warning::
    seeing=1.0 is equivalent to galpak.MUSE(psf_fwhm=1.0)
    The proper way to specify the seeing is specified in customizing-the-psf_.


The input can also be a :class:`Hyperspectral Cube <galpak.HyperspectralCube>`.
Actually, GalPaK will instantiate one from your fits file if you pass a string filename.

.. note::
    You can find other test FITS cubes in ``data/input/``.

The cube_1101 input parameters are for an arctan rotation curve:
    xo	yo	zo	radius	incl	PA	rv	Vmax	flux	Sig_o	GaussianFWHM

    15.0	15.0	15.0	4.0841	60.0	50.0	1.35	199.5	1e-16	80.0	1.0

The gk.galaxy parameters from the run above should be close to this: ::

 Galaxy Parameters : value (± stdev) [units]	 [Confidence Interval]
    x: 15.06 ± 0.08 (pixel)	 CI 95%: [14.90,15.19]
    y: 15.05 ± 0.07 (pixel)	 CI 95%: [14.91,15.20]
    z: 15.055705 ± 0.056999 (pixel)	 CI 95%: [14.948377,15.164004]
    flux: 8.41e-17 ± 2.07e-18 (same units as the input Cube)	 CI 95%: [8.14e-17,8.86e-17]
    radius: 4.10 ± 0.16 (pixel)	 CI 95%: [3.76,4.41]
    inclination: 69.74 ± 2.07 (deg)	 CI 95%: [66.64,73.99]
    pa: 125.83 ± 1.99 (deg)	 CI 95%: [121.37,129.05]
    turnover_radius: 1.37 ± 0.27 (pixel)	 CI 95%: [1.09,2.11]
    maximum_velocity: 202.74 ± 13.21 (km/s)	 CI 95%: [183.77,236.45]
    velocity_dispersion: 81.05 ± 4.68 (km/s)	 CI 95%: [72.97,93.14]

.. warning::
    The cube has units `erg/s/cm2/AA', so the galaxy flux is 8.4e-17 erg/s/cm2/AA * 1.25 Angstrom = 1.05e-16 erg/s/cm2.
    The flux is thus: ::
        gk.galaxy.flux * gk.cube.z_step
 
         

Test galpak with your cube
--------------------------

Assuming your cube has units of Angstrom (default for MUSE) : ::

        from galpak import GalPaK3D
        gk = GalPaK3D('GalPaK_cube_1101_from_paper.fits', seeing=1.0, instrument=galpak.MUSE(lsf_fwhm=2.51))
 
For MPDAF users, a `MPDAF <http://http://urania1.univ-lyon1.fr/mpdaf/>`_ ``Obj.Cube`` object is ok as input, which handles the variance : ::

        from mpdaf import obj
        objcube = obj.Cube('GalPaK_cube_1101_from_paper.fits')
        gk = GalPaK3D(objcube, seeing=1.0, instrument=galpak.MUSE(lsf_fwhm=2.51))
 
.. note::
    Currently, the variance can also be specified manually : ::

        gk = GalPaK3D('my_cube.fits',variance='my_variance.fits', seeing=1.0, instrument=galpak.MUSE(lsf_fwhm=2.51))
        
    In future version, the variance can be specified as a "STAT" or "VARIANCE" extension to the fits file.
     

Run galpak examples
-------------------

.. warning::
    From v1.9.0, you should use the :class:`DefaultModel <galpak.DefaultModel>` class as follows : ::

Assuming your cube can be read properly, you can run it with  : ::

        from galpak import GalPaK3D, DefaultModel, ModelSersic, MUSEWFM
        gk = GalPaK3D('GalPaK_cube_1101_from_paper.fits', instrument=MUSE(psf_fwhm=1.0, lsf_fwhm=2.51))
        gk.run_mcmc(max_iteration=500, model=DefaultModel(rotation_curve='arctan'))

or with the api : ::

        import galpak
        my_instrument = galpak.MUSE(psf_fwhm=1.0, lsf_fwhm=2.51)
        my_model = galpak.DefaultModel(rotation_curve='arctan')
        gk = galpak.run('galpak_125_seeing1.0_flux1e-16.fits',  instrument=my_instrument, max_iterations=500, model=my_model)

or with the autorun : ::

        import galpak
        my_instrument = galpak.MUSE(psf_fwhm=1.0, lsf_fwhm=2.51)
        my_model = galpak.DefaultModel(rotation_curve='arctan')
        gk = galpak.autorun('galpak_125_seeing1.0_flux1e-16.fits',  instrument=my_instrument, max_iterations=500, model=my_model)

and then save with : ::

        gk.save('my_galpak_run')

Typically you will need 5000 or 10000 iterations

.. warning::
    Make sure to look at the MCMC chain. Have all the parameters converged?

A practical example
-------------------

Initialize with : ::

    gk = GalPaK3D(my_file, seeing=0.8,instrument=galpak.SINFOJ250())
or
    gk = GalPaK3D(my_file, seeing=0.8,instrument=galpak.ALMA())


Check the instrument properties with : ::

    print gk.instrument

Check that it has the central wavelength ``z_central`` taken from the fits header,
which determines the right velocity 'step' (cdelt3 in km/s). If the header is not correct, you have
several options to set the central wavelength with ``z_central`` or ``cdelt3`` or ``cunit3``.

Check that the LSF and PSF parameters are ok - see below for how to tweak them.

Construct model :class:`DefaultModel <galpak.DefaultModel>` with one of the following: ::

    my_model = galpak.DefaultModel()
    my_model = galpak.ModelSersic(rotation_curve='tanh')
    my_model = galpak.ModelSersic(flux_profile='exponential')

Run with : ::

    gk.run_mcmc(model=my_model, max_iterations=7500)

Save everything with : ::

    gk.save('my_output')

and check again that the 3D kernel ``gk.psf3d`` is correct !
A wrong kernel will lead to unphysical results.



Default Model Parameters
------------------------

Both ``run`` and ``run_mcmc`` use a :class:`ModelSersic <galpak.ModelSersic>` object with exponential flux profile per default,
tanh rotation profile and thick disk dispersion.

You can see the documentation for the available parameters from the model :class:`ModelSersic <galpak.ModelSersic>` class.

.. warning::
    From v1.9.0, you should change these options in ``run_mcmc'' as follows : ::

    mydisk = galpak.DiskModel(flux_profile='gaussian', rotation_curve='isothermal')
    mydisk = galpak.Default(flux_profile='gaussian', rotation_curve='isothermal')


or using the API run_ or autorun_ method: ::

    import galpak
    my_instrument = galpak.MUSE(lsf_fwhm=2.51)
    mydisk = galpak.DiskModel(flux_profile='gaussian', rotation_curve='isothermal')
    gk = galpak.run('galpak_125_seeing1.0_flux1e-16.fits', seeing=1.0, instrument=my_instrument, model=mydisk, max_itrations=500)
    gk.save('my_galpak_run')

You can always check your model with : ::

    print(gk.model)

Run Output Overview
-------------------

The ``run_mcmc`` method returns a :class:`GalaxyParameters <galpak.GalaxyParameters>` object.

Type : ::

    print  gk.galaxy

to see the parameters (``gk.error`` contains the error vector).

Use the methods of :class:`GalaxyParameters <galpak.GalaxyParameters>` ``tofile`` or ``tolist``
to store this.

The ``run_mcmc`` also fills the ``gk`` instance parameters with several output data :

- ``gk.deconvolved_cube`` : best guess as to what the deconvolved cube should be
- ``gk.convolved_cube`` : virtually convolved cube, should be close to the inputted measure cube
- ``gk.residuals_cube`` : differential between measure cube and convolved cube, inversely scaled by measure error
- ``gk.psf3d`` : the 3D PSF*LSF used for the convolution
- ``gk.chain`` : the full markov chain, with each step holding its galaxy parameters and reduced χ
- ``gk.acceptance_rate`` : the final proportion of useful iterations in ``%``
- ``gk.initial_parameters`` : the first parameters of the markov chain
- ``gk.galaxy`` : a view to the returned :class:`GalaxyParameters <galpak.GalaxyParameters>` object
- ``gk.error`` : the error margin of above galaxy parameters
- ``gk.true_flux_map`` : the intrinsic flux map
- ``gk.true_velocity_map`` : the intrinsic velocity field
- ``gk.true_disp_map`` : the intrinsic dispersion map



Save the run
------------

Once the MCMC has run, you can save the results to file easily : ::

  import galpak
  gk = galpak.run('my_cube.fits',instrument=galpak.MUSEWFM())
  gk.save('my_run')

It will create a bunch of files prefixed by ``my_run`` in the current working directory.
See the :meth:`save() <galpak.GalPaK3D.save>` method documentation for the list of files that will be created.


Tutorials Level 1
*****************

MCMC chain tuning
-----------------
.. _random-scale:

Again, you can see the :meth:`detailed documentation for the available parameters <galpak.GalPaK3D.run_mcmc>`,
but the most important parameters to tune are :

- ``random_scale`` : a scale factor to the width of the proposal distribution (Cauchy).
  A good practice is to tune this to have an acceptance rate of 30-50 %.
  (for example, the value ``random_scale=2`` sets a factor 2x from the defaults)
- ``max_iterations`` : max number of (accepted) iterations [default=10000]
- ``method`` :  'last' or 'chi_sorted' or 'chi_min'
    Method used to determine the best parameters from the chain.
        - 'last' (default) : mean of the last_chain_fraction(%) last parameters of the chain
        - 'chi_sorted' : mean of the last_chain_fraction(%) best fit parameters of the chain
        - 'chi_min' : mean of last_chain_fraction(%) of the chain around the min chi
- ``last_chain_fraction`` : last fraction of chain (in %) to use to determine the best parameters [default=60]
- ``min_acceptance_rate`` : minimum acceptance rate (in %) to keep going. [default: 5]




Using Custom Boundaries
-----------------------

You can make sure that GalPaK will not try to find galaxy parameters outside of explicit boundaries : ::

    from galpak import run, GalaxyParameters
    min_boundaries = GalaxyParameters(x=5.)
    max_boundaries = GalaxyParameters(x=7., y=9.)
    gk = run('my_muse_cube.fits',
             min_boundaries=min_boundaries,
             max_boundaries=max_boundaries)

The boundaries you provide will be merged into the default boundaries.

.. note::
    For Vmax 'maximum_velocity', the min and max boundaires should be equal, e.g [-300,300]

Tweaking the Random Walk
------------------------

You can (and should) tweak the ``random_scale`` parameter of the ``run_mcmc`` method
in order to get an acceptance rate around 30-40 %.
The value you provide is the a coefficient *(default=1)*
applied to the random walk of the parameters.

.. figure:: images/deconvolution_example/bad_chain_not_scaled.png
   :scale: 50 %
   :alt: A bad chain, poorly scaled
   :align: center

   A bad chain, poorly scaled


But when you provide a ``random_scale`` with values greater than 1, say 5 : ::

    from galpak import GalPaK3D
    glpk3d = GalPaK3D('my_muse_cube.fits')
    galaxy = glpk3d.run_mcmc(random_scale=5.)


... you get a more excited chain :

.. figure:: images/deconvolution_example/good_chain_scaled.png
   :scale: 50 %
   :alt: A good chain
   :align: center

   A good chain with a more thorough walk

Conversely, a less-than-one ``random_scale``, in combination with ``initial_parameters``,
can be used to fine-tune your results by reducing the steps of the random walk.

Also, you can tweak the random walk of only a subset of the parameters by passing a :class:`GalaxyParameters <galpak.GalaxyParameters>` object : ::

    galaxy = glpk3d.run_mcmc(random_scale=GalaxyParameters(x=10., pa=2.))


Plotting the Markov chain
-------------------------

Once a deconvolution has been computed, you can plot the Markov chain that was created : ::

    from galpak import GalPaK3D
    glpk3d = GalPaK3D('GalPaK_cube_1101_from_paper.fits', seeing=1.0, instrument=galpak.MUSE(lsf_fwhm=2.51))
    galaxy = glpk3d.run_mcmc(max_iterations=15e3)

    # Show plot on-screen
    galpak.plot_mcmc()

    # Save plot to png or jpg file
    galpak.plot_mcmc(filepath='my_mcmc_plot.png')

.. figure:: images/deconvolution_example/GalPaK_cube_1101_from_paper_fig4.png
   :scale: 50 %
   :alt: An example of chain plotting
   :align: center

   An example of chain plotting for the GalPaK_cube_1101_from_paper.fits with N=15,000 iterations

Plotting the cross-correlations
-------------------------------

After a galpak run has been completed, you can plot the correlations in the Markov chain with : ::

    from galpak import GalPaK3D
    glpk3d = GalPaK3D('GalPaK_cube_1101_from_paper.fits', seeing=1.0, instrument=galpak.MUSE(lsf_fwhm=2.51))
    galaxy = glpk3d.run_mcmc(max_iterations=15e3)

    # Show plot on-screen
    glpk3d.plot_corner()

    # Save plot to png or jpg file
    glpk3d.plot_corner(filepath='my_correlations.png')

.. figure:: images/deconvolution_example/GalPaK_cube_1101_from_paper_fig5.png
   :scale: 50 %
   :alt: An example of chain plotting
   :align: center

   An example of chain plotting for the GalPaK_cube_1101_from_paper.fits with N=15,000 iterations

Plotting the convergence
------------------------

After a galpak run has been completed, you can plot the [Geweke's](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.27.2952) convergence diagnostic of the Markov chain with the :meth:`plot_geweke() <galpak.GalPaK3D.plot_geweke>` method: ::

    from galpak import GalPaK3D
    glpk3d = GalPaK3D('GalPaK_cube_1101_from_paper.fits', seeing=1.0, instrument=galpak.MUSE(lsf_fwhm=2.51))
    galaxy = glpk3d.run_mcmc(max_iterations=1500)

    # Show plot on-screen
    glpk3d.plot_geweke()
    # Save plot to png or jpg file
    glpk3d.plot_geweke(filepath='plot_geweke.png')

Note, this is saved automatically with the :meth:`save() <galpak.GalPaK3D.save>` method as `_geweke.png`.

The :meth:`plot_geweke() <galpak.GalPaK3D.plot_geweke>` method will also print the fraction of the chain where the z-score is less than 3sigma (``Nsigma''): ::

    INFO:GalPaK:Parameter x has converged ? 1.0
    WARNING:GalPaK:Parameter y has not converged ? 0.92
    INFO:GalPaK:Parameter z has converged ? 1.0
    WARNING:GalPaK:Parameter flux has not converged ? 0.84
    WARNING:GalPaK:Parameter radius has not converged ? 0.64
    INFO:GalPaK:Parameter sersic_n has converged ? 1.0
    INFO:GalPaK:Parameter inclination has converged ? 1.0
    INFO:GalPaK:Parameter pa has converged ? 1.0
    INFO:GalPaK:Parameter turnover_radius has converged ? 1.0
    INFO:GalPaK:Parameter maximum_velocity has converged ? 1.0
    INFO:GalPaK:Parameter velocity_dispersion has converged ? 1.0

This is also saved automatically with the :meth:`save() <galpak.GalPaK3D.save>` method as `_galaxy_parameters_convergence.dat`.

.. figure:: images/plot_geweke.png
   :alt: An example of a Geweke diagnostic plot
   :align: center



Plotting the cubes' images
--------------------------

Once a deconvolution has been computed, you can plot the resulting cubes : ::

    from galpak import GalPaK3D
    glpk3d = GalPaK3D('my_muse_cube.fits')
    galaxy = glpk3d.run_mcmc()

    # Show plot on-screen
    galpak.plot_images()

    # Save plot to png or jpg file
    galpak.plot_images(filepath='my_plot.png')

    # Crop the rendered cubes along z, around the galaxy's z
    galpak.plot_images(z_crop=7)

.. figure:: images/deconvolution_example/plot_images.png
   :scale: 100%
   :alt: An example of images plotting
   :align: center

   An example of images plotting


Recover the parameters from an earlier save
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you've saved the run to disk, you can use the following ``from_file`` method to read the parameters: ::

   params = GalPaK3D.GalaxyParameters()
   params.from_file('my_param_file.dat')


Recover the chain from an earlier save
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Once you've saved the run to disk, you can use the following snippet to re-iterate through the chain: ::

  import asciitable
  with open('my_run_chain.dat', 'r') as chain_file:
      data = asciitable.read(chain_file.read(), Reader=asciitable.FixedWidth)
  for data_record in data:
      # <your logic here>
      print(data_record.x)
      print(data_record.reduced_chi)

or simpy using the ``import_chain`` method: ::

   glpk3d = GalPaK3D('my_muse_cube.fits')
   glpk3d.import_chain('my_chain.dat')


Cubes from another instrument
-----------------------------

You can specify the instrument that will convolve the simulated data. ::

  import galpak
  gk = galpak.run('my_musenfm_cube.fits', instrument=galpak.MUSENFM())

Instruments accept two parameters: ``psf`` and ``lsf`` : ::

  from galpak import run, MUSENFM, GaussianPointSpreadFunction, GaussianLineSpreadFunction
  my_psf = GaussianPointSpreadFunction(fwhm=1.2, pa=0., ba=1.0)
  my_lsf = GaussianLineSpreadFunction(fwhm=0.00065)
  gk = run('my_musenfm_cube.fits', instrument=MUSENFM(psf=my_psf, lsf=my_lsf))

By default, the instrument will combine the ``psf`` (2D) and the ``lsf`` (1D) into a 3D spread function
and will apply it to the cube in the method :meth:`convolve(cube) <galpak.Instrument.convolve>`.

:ref:`More details about the instruments. <instruments-page>`

Tutorials Level 2
*****************
Setting a parameter to a fixed value 
------------------------------------

.. _fixed-value:

You can use the parameter ``known_parameter``, which takes a :class:`GalaxyParameters <galpak.GalaxyParameters>` as in the example here: ::

   import galpak
   fixed = galpak.GalaxyParameters().copy()
   fixed.turnover_radius = 1
   gk = GalPaK3D('GalPaK_cube_1101_from_paper.fits', seeing=1.0, instrument=galpak.MUSE(lsf_fwhm=2.51))
   gk.run_mcmc(max_iteration=500,known_parameters=fixed)


Using line doublets
-------------------

You can use the parameter ``line``, a dictionary, to tell galpak you're expecting a dual peak : ::

  from galpak import GalPaK3D
  glpk3d = GalPaK3D('my_muse_cube.fits', line={'wave': [3726.2, 3728.9], 'ratio': [0.8, 1.0]})
  galaxy = glpk3d.run_mcmc()

or using the API : ::

  from galpak import GalPaK3D
  res = GalPaK3D.run('my_muse_cube.fits', line={'wave': [3726.2, 3728.9], 'ratio': [0.8, 1.0]})

.. note::
    Only the rest-wavelengths are needed regardless of redshift because the algorithm works in velocity space. Here, you specify the velocity difference for the two lines in the doublet, ``3e5*(l2-l1)/(l1+l2)*2``, so the redshift does not matter.

.. warning::
  For version >= 1.9.0, this ``line`` parameter is now part of the :class:`DiskModel <galpak.DiskModel>` class.

So for GalPaK3D v1.9.0 and beyond, the line should be used as : ::

  from galpak import GalPaK3D, DiskModel
  myline = {'wave': [3726.2, 3728.9], 'ratio': [0.8, 1.0]}
  glpk3d = GalPaK3D('my_muse_cube.fits')
  galaxy = glpk3d.run_mcmc(model=DiskModel(line=myline))


or using the API ::

  from galpak import GalPaK3D, DiskModel
  myline = {'wave': [3726.2, 3728.9], 'ratio': [0.8, 1.0]}
  disk = DiskModel(line=myline)
  res = GalPaK3D.run('my_muse_cube.fits', model=disk )

.. note::
    For version = 1.9.0, this ``line`` parameter can also be used as in prior versions.



.. _customizing-the-psf:

Customizing the Point Spread Function
-------------------------------------

Tweaking the PSF
~~~~~~~~~~~~~~~~

You can either specify the seeing parameter as in the example above,
or change its attributes from the Instrument parameters : ::

    from galpak import GalPaK3D, SINFOK250, GaussianPointSpreadFunction

    # this one-liner
    my_instrument = SINFOK250(psf=GaussianPointSpreadFunction(fwhm=0.7,pa=0.1,ba=0.9))

    # is equivalent to
    my_instrument = SINFOK250()
    my_instrument.psf.fwhm = 1.5
    my_instrument.psf.pa = 0.1
    my_instrument.psf.ba = 0.9

    # and, as the gaussian PSF is the default, you can also fast-tweak it this way
    my_instrument = SINFOK250(psf_fwhm=0.7, pa=0.1, ba=0.9)

    # then, whatever way you used to create your instrument, use it like this
    glpk3d = GalPaK3D('my_sinfok250_cube.fits', instrument=my_instrument)
    galaxy = glpk3d.run_mcmc()


De-activating the PSF
~~~~~~~~~~~~~~~~~~~~~

You can de-activate the PSF entirely : ::

    from galpak import GalPaK3D, SINFOK250, NoPointSpreadFunction

    glpk3d = GalPaK3D('my_sinfok250_cube.fits', instrument=SINFOK250())
    glpk3d.instrument.psf = None
    galaxy = glpk3d.run_mcmc()

    # ... is the same as
    glpk3d = GalPaK3D('my_sinfok250_cube.fits', instrument=SINFOK250())
    glpk3d.instrument.psf = NoPointSpreadFunction()
    galaxy = glpk3d.run_mcmc()


Using another PSF
~~~~~~~~~~~~~~~~~

You can specify another PSF you want to use with the instrument : ::

    from galpak import GalPaK3D, SINFOK250, MoffatPointSpreadFunction

    glpk3d = GalPaK3D('my_sinfok250_cube.fits', instrument=SINFOK250())
    glpk3d.instrument.psf = MoffatPointSpreadFunction(
        alpha=1.11,  # (uninformed/dummy example value)
        beta=2.22    # (uninformed/dummy example value)
    )

The ``galpak`` module provides :class:`GaussianPointSpreadFunction <galpak.GaussianPointSpreadFunction>` and
:class:`MoffatPointSpreadFunction <galpak.MoffatPointSpreadFunction>`.
They each have a number of parameters you may provide upon instantiation.

If you don't, default values inferred from the Instrument and Cube will be used : ::

    glpk3d = GalPaK3D('my_muse_cube.fits')
    print glpk3d.instrument.psf

    # psf = Gaussian PSF :
    #   fwhm         = 0.8 "
    #   pa           = 0 °
    #   ba           = 1.0


.. _make-your-own-psf:


Using custom image for the PSF
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify an empirically determined PSF (e.g. from a bright star) using
the class :class:`ImagePointSpreadFunction <galpak.ImagePointSpreadFunction>`
which accepts fits file or ndarray : ::

    import galpak
    my_psf = galpak.ImagePointSpreadFunction('my_psf_image.fits')
    gk = galpak.GalPak3D('my_cube.fits', instrument=galpak.MUSEWFM())
    gk.instrument.psf = my_psf
    print gk.instrument

    #psf = Custom Image PSF
    #lsf = Gaussian LSF : fwhm = 2.675  Angstrom


or : ::

    import galpak, pyfits
    image_array = pyfits.open('my_psf_image.fits')[0].data
    instrum = galpak.MUSEWFM(psf=galpak.ImagePointSpreadFunction(image_array) )
    gk = galpak.GalPak3D('my_cube.fits', instrument=instrum)
    print gk.instrument

    #psf = Custom Image PSF
    #lsf = Gaussian LSF : fwhm = 2.675  Angstrom

.. warning::
    The custom PSF image must be well centered, otherwise the centroid positions will be off. Ideally, (xo, yo) should be : ::

        xo = (shape[1] - 1) / 2 - (shape[1] % 2 - 1)
        yo = (shape[0] - 1) / 2 - (shape[0] % 2 - 1)
    where shape is the image shape (which should be the same shape as the cube.shape[1:] spatial dimensions).

.. _use-custom-image-psf:

Making your own PSF
~~~~~~~~~~~~~~~~~~~

You can create your own PSF, it just needs to implement :class:`PointSpreadFunction <galpak.PointSpreadFunction>`.

A good example of this is the ``NoPointSpreadFunction`` class : ::

    from galpak import PointSpreadFunction


    class NoPointSpreadFunction(PointSpreadFunction):
        """
        A spread function that does not spread anything, and will leave the cube unchanged.
        Passing this class to the instrument's psf is the same as passing None.
        """
        def __init__(self):
            pass

        def as_image(self, for_cube):
            """
            Return the identity PSF, chock-full of zeros.
            """
            # Here, you may create your own 2D PSF image and then return it
            shape = for_cube.shape[1:]
            return np.zeros(shape)



.. _customizing-the-lsf:

Customizing the Line Spread Function
------------------------------------

Using another LSF
~~~~~~~~~~~~~~~~~

You can specify another LSF you want to use with the instrument : ::

    glpk3d = GalPaK3D('my_muse_cube.fits', instrument=MUSEWFM(lsf=MUSELineSpreadFunction()))

The ``galpak`` module provides :class:`GaussianLineSpreadFunction <galpak.GaussianLineSpreadFunction>` and
:class:`MUSELineSpreadFunction <galpak.MUSELineSpreadFunction>`.
They each have a number of parameters you may provide upon instantiation.


.. _make-your-own-lsf:

Making your own LSF
~~~~~~~~~~~~~~~~~~~

You can create your own LSF, it just needs to implement :class:`LineSpreadFunction <galpak.LineSpreadFunction>`.


Creating a custom instrument
----------------------------

You can also create your own instrument, by extending :class:`galpak.Instrument <galpak.Instrument>`.
You can override the ``calibrate`` and ``convolve`` methods : ::

    from galpak import Instrument


    class MyInstrument(Instrument):

        # This callback is called by GalPaK3D during its init
        def calibrate(self, cube):
            """
            The cube is a HyperspectralCube, and
            it has additional attributes provided by GalPaK3D :
                - xy_step (in ")
                - z_step (in µm)
                - z_central (in µm)
            """
            # <Your logic here>
            # Important : run the default calibration in the end
            Instrument.calibrate(self, cube)

        # Optionally, you may override the convolution method
        # By default it applies the PSF3D, see Instrument implementation
        def convolve(self, cube):
            """
            Convolve the provided data cube.
            Should transform the input cube and return it, it is faster than copying.
            """
            # <convolve the cube>
            return cube



.. note::
    If you do create your own instrument, please consider making a pull request !

.. _adding_galaxy_parameter:

Adding another Galaxy Parameter
-------------------------------

.. note::
    This is for advanced users only.

The file you want to edit is ``lib/galaxy_parameters.py``.

Say you want to add a new galaxy parameter named ``sugar`` :

1. Update the list ``GalaxyParameters.names``, add 'sugar' at the end.
2. Add the property after the others : ::

       sugar = GalaxyParameter(name='sugar', key=10, doc="Some more sugar", unit="sweetness", precision="3.2f")

   Here are the parameters you can provide the describe the new galaxy parameter :

     - name (string) : the name of the variable (MUST be the same as the name in ``GalaxyParameters.names``.)
     - key (int) : the position in the the ndarray of this parameter
     - short (string) : a shorter name, for compact display
     - doc (string) : some documentation that will appear to the enduser.
     - unit (string) : the unit, if any
     - precision (string) : the precision to use during string casting, as used by ``string.format()``.

3. Update this class' ``__init__()`` method (signature and assignation)
4. Update this class' ``__new__()`` method  (signature and call to ``__init__``)


Tutorials Level 3
*****************
.. _reading_old_parameters:

Reading old parameter file
--------------------------

If you want to read the output parameters from an old run, you can do so: ::

    gk=galpak.GalPak3D(mycube_name,instrument=myinstrument)
    gk.galaxy.from_file(prefix+'_galaxy_parameters.dat')
    gk.galaxy


If you want to use an array to set parameters (in order to change the boundaries, e.g.), you can do so: ::

    from galpak import GalaxyParameters
    gp = GalaxyParameters.from_ndarray(my_ndarray_of_data)

You can also convert the parameters to an astropy.table: ::

    t = gk.galaxy.as_table()

or turn it into a vector ndarray: ::

    v = gk.galaxy.as_vector()

.. _reading_old_chains:

Reading old chain, recomputing parameters
------------------------------------------

If you want to read an old run and recompute the parameters using a different method or settings: ::

    gk=galpak.GalPak3D(mycube_name,instrument=myinstrument)
    gk.import_chain(prefix+'_chain.dat', compute_best_parameters=True)
    gk.galaxy

this will use the ``best_parameters_from_chain`` method to compute the galaxy parameters, with the parameters (method='last', chain_fraction=60, percentile=95).
If you want to customize further: ::

    gk=galpak.GalPak3D(mycube_name,instrument=myinstrument)
    gk.import_chain(prefix+'_chain.dat', compute_best_parameters=False)
    gk.best_parameters_from_chain(method_chain='last', chain_fraction=40, percentile=68)
    gk.galaxy

.. _handling_short_parameter_names:

Handling of parameter names
---------------------------

You can construct a dictionary of shortcut names for each of the parameter: ::

    my_dict = gk.galaxy.short_dict()

Or access each as: ::

    short = gk.galaxy.__shorts__('inclination')


Tutorials Level 4
*****************
.. _changing_statistics:

Changing of chi2 statistics
---------------------------

GalPak3D accepts the following statistics to perform the parameter optimization, which can be set with the parameter `chi_stat':

- "gaussian" [default] to perform the sum of residual squares (aka. normal chi2), i.e. sum ( D_i - M_i )^2 / stdev_i^2

When the noise in the data is poissonian, the following options are available:

.. warning::
    This is experimental and has not been validated. Please use with caution and send feedback.

- "Neyman" using the Modified Neyman statistic from `Humphrey 2009 <http://adsabs.harvard.edu/abs/2009ApJ...693..822H>`_, i.e.  Sum ( M_i - D_i )^2 / max(D_i,1)

- "Pearson" using the Pearson statistic  `Humphrey 2009 <http://adsabs.harvard.edu/abs/2009ApJ...693..822H>`_,  i.e.  Sum ( M_i - D_i )^2 / M_i

- "Mighell" using the Mighell modified Statistic `Mighell 1998 <http://adsabs.harvard.edu/abs/1999ApJ...518..380>`_, i.e. Sum ( D_i + min(1,D_i) - M_i)^2 / D + 1

- "Cstat" using the Cash-statistic from Cash 1979 described in `Humphrey 2009 <http://adsabs.harvard.edu/abs/2009ApJ...693..822H>`_, i.e.  Sum ( M_i - D_i + D_i * log(D_i/M_i) )

