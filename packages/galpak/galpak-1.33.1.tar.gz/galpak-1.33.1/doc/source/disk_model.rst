Disk Models
***********

Model Handling
~~~~~~~~~~~~~~

You should define the model with the :class:`ModelSersic() <galpak.ModelSersic>` class : ::

    from galpak import GalPaK3D, ModelSersic
    mymodel = ModelSersic(flux_profile='exponential',rotation_curve='tanh',redshift=1.0)
    gk = GalPaK3D('GalPaK_cube_1101_from_paper.fits',model=mymodel)

And ``print(gk.model)`` should yield

| [MODEL] :
|  type = ModelSersic
|  flux_profile = exponential
|  rotation_curve = tanh
|  thickness_profile = gaussian
|  dispersion_profile = thick
|  line = None
|  aspect = None
|  redshift = 1.0
|  pixscale = None
|  cosmology = planck15
|  logger = <Logger GalPaK: DiskModel: (INFO)>
|  h = 0.6774
|  Ez = 1.7786701537924485
|  DeltaVir = 157.83616517152367
|  halo = <module 'colossus.halo' from '/usr/local/lib/python3.7/site-packages/colossus/halo/__init__.py'>
|  kpc = 8.231853271026885
|  q = 0.15

.. note::
    The galpak :meth:`save() <galpak.GalPaK3D.save>` method will save a file model.txt

If the model is saved into a model.txt file, one can use : ::

    from galpak import GalPaK3D
    gk = GalPaK3D('GalPaK_cube_1101_from_paper.fits',model='model.txt')

The file model.txt should be like :

| [MODEL] :
|  type = ModelSersic
|  flux_profile = exponential
|  rotation_curve = tanh
|  thickness_profile = gaussian
|  dispersion_profile = thick
|  line = None
|  aspect = None
|  redshift = 1.0

Base Model Class
~~~~~~~~~

.. autoclass:: galpak.DefaultModel

.. autoclass:: galpak.ModelSersic

.. autoclass:: galpak.DiskModel
    :members: __dict__