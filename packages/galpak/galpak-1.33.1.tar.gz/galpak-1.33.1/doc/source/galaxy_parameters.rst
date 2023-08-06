
.. important::
    A description of the parameter meaning can be found `here <galaxy_parameters.html#description>`_

-----


.. autoclass:: galpak.GalaxyParameters
    :members: from_ndarray, short_info, long_info


Description
~~~~~~~~~~~

A ``GalaxyParameters`` object ``gp`` is merely a glorified ``numpy.ndarray`` with convenience accessors and mutators :

+------------------------+---------------------------------------------------------------------------------------------+
| Component              | Description                                                                                 |
+========================+=============================================================================================+
| gp.x                   | X coordinates of the center of the galaxy. (in pixels)                                      |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.y                   | Y coordinates of the center of the galaxy. (in pixels)                                      |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.z                   | Z coordinates of the center of the peak. (in pixels)                                        |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.flux                | Sum of the values of all pixels. (in the unit of the cube)                                  |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.radius              | Radius of the galaxy. (in pixels)                                                           |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.inclination |br|    | Inclination of the galaxy (in degrees),                                                     |
| gp.pitch               | aka. pitch along observation axis.                                                          |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.pa |br|             | Position Angle, clockwise from Y (in degrees),                                              |
| gp.roll                | aka. roll along observation axis.                                                           |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.rv |br|             | turn-over radius (in pixels). (meaning is model dependent)                                           |
| gp.turnover_radius     |                                                                                             |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.maximum_velocity    | Maximum Velocity. (in km/s)                                                                 |
+------------------------+---------------------------------------------------------------------------------------------+
| gp.velocity_dispersion | Disk Dispersion spatially constant (in km/s) added in addition to kinematics dispersion.    |
| |br| gp.sigma0         |                                                                                             |
+------------------------+---------------------------------------------------------------------------------------------+

.. warning::
    the velocity_dispersion parameter is NOT the total dispersion. This parameter is akin to a turbulent term. It is added in quadrature to the dispersions due to the disk model and to the thickness.
    See Cresci et al. 2009, Genzel et al. 2011, and `Bouche et al. 2015 <http://adsabs.harvard.edu/abs/2015AJ....150...92B>`_

You still can access the parameters like an indexed array ::

    assert gp.x == gp[0]  # true
    assert gp.y == gp[1]  # true
    # ...
    assert gp.sigma0 == gp[9]  # true


You may instantiate a ``GalaxyParameters`` object like so ::

    from galpak import GalaxyParameters

    gp = GalaxyParameters(z=0.65)
    gp.x = 5.
    assert gp.z == 0.65       # true
    assert gp.x == 5.         # true


.. warning::
    An undefined value in ``GalaxyParameters`` will be ``nan``, not ``None`` ::

        assert math.isnan(gp.pa)  # true
        assert gp.pa is None      # false


Getting the Wavelength
~~~~~~~~~~~~~~~~~~~~~~

The ``z`` attribute in a ``GalaxyParameter`` is in pixels,
you may want the value in the physical unit specified in your Cube's header.

To that effect, you may use the ``wavelength_of`` method of the ``HyperspectralCube``: ::

        from galpak import GalPaK3D
        gk = GalPaK3D('my_muse_cube.fits')
        gk.run_mcmc()

        wavelength = gk.cube.wavelength_of(gk.galaxy.z)

