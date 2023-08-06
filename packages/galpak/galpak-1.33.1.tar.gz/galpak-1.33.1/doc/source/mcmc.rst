MCMC
****

GalPaK3D allows the user to select several samplers for the MCMC as described in the
:meth:`run_mcmc <galpak.run_mcmc()>` method which has the following options:

        mcmc_method: 'galpak' [default] | 'emcee_walkers'| 'emcee_MH' | 'dynesty' | 'multinest'
            The MCMC method.
                - galpak:   for the original MCMC algorithm using Cauchy proposal distribution
                - emcee_MH: emcee v2.x classic MH; no longer supported
                - emcee_walkers: emcee v3.x multi-Walkers algorithms with Moves
                - dynesty: unsupported
                - multinest: still experimental
                - pymc3: to be implemented

        mcmc_sampling:
                - galpak: 'Cauchy' [default] | 'Normal' | 'AdaptiveCauchy'
                - emcee_walkers: 'walkers' [default] | 'walkersCauchy' | 'DE' | 'Snooker' | 'Cauchy' | 'Normal'
                - multinest: None
                - pymc3: to be implemented
            The proposal sampling methods

.. figure:: images/GalPaK_MCMC.png
     :scale: 60%
     :align: center

GalPaK3D uses an internal :class:`MCMC <galpak.MCMC>` class which extend the galpak class.
This can be used to call its likelihood such as : ::
    li = gk(params)

using a :meth:`self.__call__() <MCMC.__call__>` method which returns the lnprob


Here is a full example: ::

    import galpak
    gk=galpak.GalPaK3D('data/input/GalPaK_cube_1101_from_paper.fits',model=galpak.DefaultModel())
    p=gk.model.Parameters()
    params=p.from_ndarray([15,15,15,1e-16,5,60,90,1,100,10])
    li=gk(params)

You can always check that the log-likelihood is finite : ::

    print(li)
    -16117.55742040931

If it is not finite, this is probably caused by the priors when the parameter values are outside the min and max boundaries.


.. autoclass:: galpak.MCMC
    :members: as_image


