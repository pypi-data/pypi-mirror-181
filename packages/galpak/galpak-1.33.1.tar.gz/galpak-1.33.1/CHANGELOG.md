1.33.1 2022-11-09
-----------------
 - python 3.10 compatibility

1.33.0 2022-10-08
-----------------
 - astropy 5.1 compatibility
 - default AdaptiveCauchy for run API
 
1.32.2 2022-07-25
-----------------
 - proper thickness normalization for thickness_profile
 - fix bug zcrop in plot_images 
 
1.32.0 2022-02-01
-----------------
 - added MAOPPY PSF fitter; updates from maoppy version 1.5.0
 - added MAOPPY PSF from https://gitlab.lam.fr/lam-grd-public/maoppy 
 
1.31.0 2021-07-26
-----------------
 - bug fix in handling PSF centering. Consequence of 0.5 pixel shifts if even spaxels
 - bug fix in handling LSF centering. Consequence of 0.5 pixel shifts if even array

1.30.6 2021-06-16
-----------------
 - bug fix in handling manual variance

1.30.5 2021-05-13
---------------
 - bug fix in read_model
 - save input filenames in run.txt
 - multinest outpath option
 - added tests
 
1.30 2020-10-06
---------------
 - revamped test suite
 - better import handling with src/
 - few minor bug fixes
 - Now available on [pypi](https://pypi.org/project/galpak)
 
1.29 2020-09-10
---------------
 - bug in read instrument Generic
 
1.28 2020-05-03
---------------
 - bug in colormap for true/obs_maps
 
1.27 2020-04-03
---------------
 - bug in read_instrument .txt for ALMA
 - bug in PA circularization 
 - better handling pixscale in instruments

1.24 2020-02-24
--------------
 - change Vmin/Vmax; 
 - handling circularity pa improvement
 - revamped api
 - bug fix map indices as floats; impact only for compact galaxies
 - NEW option to use flux user-defined map ; as string or ndarray
 - NEW option mcmc_sampling to use combo walkers+Cauchy with Emcee [doc](/doc/under_the_hood.html#mcmc)
 - NEW option mcmc_sampling AdaptiveCauchy to adapt Cauchy sampling automatically [doc](/doc/under_the_hood.html#mcmc)
 - NEW option mcmc_method to use multinest [doc](/doc/under_the_hood.html#mcmc)
 - revamped EMCEE (>3.0 only) with mixed Cauchy and StretchMove sampling law

1.20 2019-10-21
---------------
 - NEW option mcmc_method to use emcee MH or walkers [doc](/doc/under_the_hood.html#mcmc)
 - NEW method_chain option MAP (Maximum A Posteriori)
 - NEW added BIC, AIC compute_stats method
 - NEW string parser to read/write Model in a CONFIG file  [doc](/doc/under_the_hood.html#model-handling)
 - NEW string parser to read/write Instrument in a CONFIG file [doc](/doc/under_the_hood.html#instruments-handling)
 - more robust handling of nan
 - better obs_maps convolution with astropy fft
 - added default lsf(lambda) for MUSE 
 - plot_correlation removed / use plot_corner
 - plot_mcmc saved for both sorted and unsorted
 - removed chain error maps

1.16.0 2019-07-15
-----------------
 - added Freeman, NFW, Burkert, Spano [doc](/doc/under_the_hood.html#base-model-class)
 - revamped model_class
 - added boundaries limits to plot_mcmc
 - bug fix in convolution when some pixels are nan

1.14.0 2019-07-05
-----------------
 - fix bug in display Mdyn
 - fix API logger autorun 
 - fix bug in display obs_maps (removed moment_maps) using [Epinat+2010](https://doi.org/10.1111/j.1365-2966.2009.15688.x)

1.12.0 2019-04-28
-----------------
 - fix bug in PSF PA

1.11.0 2019-04-05
-----------------
 - New autorun in api to autotune random_scale [doc](/doc/api.html#galpak.autorun)
 - New HARMONI class
 - added model utilities plot_vprofile & plot_SBprofile
 - added cosmology method to model class (Experimental)
 - New Extentions class for V22, dvdx

1.10.2 2019-04-02
-----------------
 - save geweke convergence into convergence.dat [doc](/doc/tutorials.html#plotting-the-convergence)

1.10.1 2019-03-14
------------------
 - plot geweke diagnostic added
 - added error maps
 - bug in test reference
 - bug when using noLineSpreadFunction

1.10 -- 2019-02-09
-------------------
 - python >3.5 full compatibility
 - revamped test suites
 - slight improved performances diskmodel / psfextrude

1.9.1 -- 2018-08-01
-------------------
 - bug fix in plot_corner if corner not present
 - fix small issue in obs/true maps

1.9.0 -- 2018-04-13
-------------------
 - bug fix in xy_step from cube when RA/Dec not co-aligned with pixels
 - enforcing Vmax>0, PA [0, 360]
 - improvements on h step
 - moved disk calculations to NEW model class [DiskModel](/doc/under_the_hood.html#disk-models)
 - moved line to model class
 - added best chi2 in output

1.8.8 -- 2018-03-18
-------------------
 - Generic instrument added default spaxel & cdelt sizes
 - fix significant bug in 'mass' rotation_curve for exponential profiles
 - added Sersic n=2 flux_profile as 'sersicN2'
 - ensured compatibility with numpy >= 1.14
 - ensured compatibility with Python3
 - improvements in doc on parameter meaning

1.8.7 -- 2018-02-16
-------------------
 - added as_vector and as_table methods to GalaxyParameters class.
 - added tutorial info on rereading chains/parameters.
 - fixed bug in PA handling around +/-180 using circular statistics
 - migrated from asciitable to astropy.io.ascii
 - added corner plot
 - added tutorial info regarding other statistics [expiremental]
 - fixed bug in Vmax min/max boundaries (enforcing they be equal)


1.8.6 -- 2018-01-28
-------------------
 - updates to tutorial regarding variance input
 - major overall of variance handling
 - fix verbose bug in run api.

1.8.5 -- 2017-09-12 (formally 1.9.1)
-------------------
 - fixed handling of variance

1.8.4 -- 2017-07-13 (formally 1.9.0)
-------------------
 - fixed a few ident and \t issues
 - fixed api
 - updated tutorial example
 - update papers.md

1.8.3 -- 2017-04-10
-------------------
 - allow either alpha or FWHM for MOFFAT; both in arcsec

1.8.2 -- 2017-03-21
-------------------
 - Fixed minor bugs when both CD3_3 and CDELT3 present
 - Added FWHM to MOFFAT PSF; moved MOFFAT alpha to arcsec

1.8.1 -- 2017-02-15
-------------------
 - Fixed several minor bugs in plot_true_maps and plot_obs_maps (added slit)

1.8.0 -- 2017-02-13
-------------------
 - Fixed a major bug for compact galaxies (a RunTime error div 0) which lead to occasional Chi2=0, and reduced length of chains
 - Improved MUSELineSpreadFunction LSF handling (FWHM computed from moments)

1.7.1 -- 2017-02-09
-------------------
 - Fixed a bug with writeto with MaskedArrays in Hyperspectral
 - Allow the possibility to set Cube.var=None to force the variance out

1.7.0 -- 2016-07-14
-------------------
 - Fixed a bug in observed moment & dispersion maps for line singlets ; convolved_cube unaffected

1.6.8 -- 2016-05-23
-------------------

 - Fixed a bug in saving chain
 - Fixed a bug in syntax boolean check for psf from an image (and re-normalized)
 - Fixed a bug in observed moment & dispersion maps for line doublets; convolved_cube unaffected

1.6.7 -- 2016-03-30
-------------------

 - Fixed a bug for 'observed moment maps' for saved observed maps.fits

1.6.6 -- 2016-03-17
-------------------

 - Fixed a bug for 'observed moment maps' for doublets like OII

1.6.5 -- 2016-03-02
-------------------

 - Added support to save 'observed moment maps'

1.6.4 -- 2016-01-16
-------------------

 - minor bug fix in api; swap orders in get_steps

1.6.3 -- 201508-25
-------------------

 - Added support for Poisson statistics

1.6.2 -- 2015-08-19
-------------------

- Adding ISOthermal rotation curve

1.6.1 -- 2015-07-08
-------------------

- minor bug fixes


1.6.0 -- 2015-05-28
-------------------

- change max_boundaries for the 1/2 light radius to 3/8th of cube_size in pixels [was set to 4"]
- bug fix at the central pixel of the model [showed up when half-light radius is very small < 2pixels]
- remove hidden call with atpy to asciitable
- updated tutorial with file used in paper.
- fix issues with setup.py
- fix small issues with custom PSF images

1.5.0 -- 2015-05-15
-------------------

- Add a `setup.py` using `distutils`.
- Implement `doit` tasks (for developer only):
    - `doit website`, or just `doit`, to rebuild the whole website.
    - `doit tarball`, to rebuild the distributed tarball.
    - `doit publish` to upload the website to the remote server.
    - `doit all` to do it all: _doc, tarball, website, publication_
- Fix the test suite, which is now ran with the simple `nosetests` command.


1.4.7 -- 2015-05-11
-------------------

- Added upper/lower confidence intervals on galaxy parameters from custom
  percentiles [default = 95%]. (specified with percentile parameter to run_mcmc)
- Make `plot_mcmc` show `-log[chi2]` with `plot_mcmc(plot_likelihood=True)`.
- Add `hz_profile` [profile perpendicular to disk] `gaussian` [default] `exponential` or `sech2`.
- Add a `read_files` method.


1.4.6 -- 2015-02-19
-------------------

- Revert to anti-clockwise for `PSF_PA`.
- Fix minor bug in min/max boundaries.


1.4.5 -- 2014-12-24
-------------------

- Add support for hyperbolic rotation curve `tanh()`.


1.4.4 -- 2014-12-20
-------------------

- Change the default chain fraction to 60%.


1.4.3 -- 2014-12-15
-------------------

- Add a generic `Instrument` with no defaults.
- Fix a bug introduced in 1.4.1 for `initial_parameters`.


1.4.2 -- 2014-12-12
-------------------

- Add `KMOS` Instrument support.
- Revamp the documentation.


1.4.1 -- 2014-12-10
-------------------

- Improve support of `CUNIT`.
- Fix a bug introduced with `1.3.0`.


1.3.0 -- 2014-12-09
-------------------

- Add `ALMA` Instrument support.


1.2.0 -- 2014-11-01
-------------------

- Add `film_images()` video generator.


1.1.3 -- 2014-10-22
-------------------

- Add `ImagePointSpreadFunction`.
- Add `VectorLineSpreadFunction`.
- Removed interpolation on velocity plots.


1.1.2 -- 2014-10-17
-------------------

- Fix issue with `true_maps` image origin.
- Update the documentation.


1.1.1 -- 2014-10-13
-------------------

- Add `GalaxyParameters.PA` accessor alias.
- Fix matplotlib's "math domain error" issue that happened in various plots.


1.1.0 -- 2014-10-10
-------------------

- Easen the process of adding a new `GalaxyParameter`.


1.0.4 -- 2014-10-01
-------------------

- Add support for `CD3_3` header card.
- Add `3dkernel` as output.
- Minor edits.


1.0.2 -- 2014-09-09
-------------------

- Add support for OII/OIII/SII doublets (and others).


1.0.1 -- 2014-07-07
-------------------

- Bugfixes.
- More bugfixes.
- Website http://galpak.irap.omp.eu/


1.0.0 -- 2014-05-05
-------------------

- Initial release of galpak.
