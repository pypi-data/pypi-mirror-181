# -*- coding: utf-8 -*-

import numpy as np
import importlib.util
from scipy.interpolate import RectBivariateSpline, InterpolatedUnivariateSpline, interp2d

try:
    from astropy.io import fits
except ImportError:
    import pyfits as fits

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GalPaK: PSF')
#
# This file contains the PointSpreadFunction and LineSpreadFunction interfaces
# as well as some basic implementations of these interfaces :
#   - Gaussian PSF
#   - Moffat PSF
#   - Gaussian LSF
#   - MUSE LSF (only if mpdaf module is available)
#
# The instrument will use both 2D PSF and 1D LSF
# to create a 3D PSF with which it will convolve the cubes.
#


## POINT SPREAD FUNCTIONS ######################################################


class PointSpreadFunction:
    """
    This is the interface all Point Spread Functions (PSF) should implement.
    """

    logger = logger

    def as_image(self, for_cube):
        """
        Should return this PSF as a 2D image shaped [for_cube].

        for_cube: HyperspectralCube
            Has additional properties computed and attributed by GalPaK :
                - xy_step (in ")
                - z_step (in µm)
                - z_central (in µm)

        :rtype: ndarray
        """
        raise NotImplementedError()

    def _radius(self, xo, yo, x, y):
        """
        Computes the radii, taking into account the variance and the elliptic shape
        """
        dx = xo - x
        dy = yo - y
        # Rotation matrix around z axis
        # R(90)=[[0,1],[-1,0]] so anti-clock-wise y -> x & x -> -y
        radian_pa = np.radians(self.pa)
        dx_p = dx * np.cos(radian_pa) + dy * np.sin(radian_pa)
        dy_p = -dx * np.sin(radian_pa) + dy * np.cos(radian_pa)

        return np.sqrt(dx_p ** 2 / self.ba ** 2+ dy_p ** 2 )

class NoPointSpreadFunction(PointSpreadFunction):
    """
    A point spread function that does not spread anything, and returns the cube unchanged.
    Passing this to the instrument's psf is the same as passing None.
    """
    def __init__(self):
        pass

    def as_image(self, for_cube):
        """
        Return the identity PSF, chock-full of ones.
        """
        shape = for_cube.shape[1:]
        return np.ones(shape)


class ImagePointSpreadFunction(PointSpreadFunction):
    """
    A custom point spread function using a provided 2D image
    that should have the same shape as the cube's (x,y) and
    centroid should be at
        xo = (shape[1] - 1) / 2 - (shape[1] % 2 - 1)
        yo = (shape[0] - 1) / 2 - (shape[0] % 2 - 1)

    """
    def __init__(self, image_2d):
        """
        accepts fits file or ndarray

        """
        if isinstance(image_2d, str):
            self.filename = image_2d
            my_image = fits.open(image_2d)
            if my_image['PRIMARY'].data is not None:
                 image_2d = my_image['PRIMARY'].data
                 header = my_image['PRIMARY'].header
            elif my_image['DATA'].data is not None:
                 image_2d = my_image['DATA'].data
                 header = my_image['DATA'].header

        elif isinstance(image_2d,np.ndarray):
             image_2d = image_2d
             self.filename = str(image_2d.__class__)
        else:
            raise ValueError(' PSF provided is not a fits file nor an array !!')

        logger.info( "Normalizing PSF image")
        self.image_2d =  image_2d /  image_2d.sum()
        self.header = header

        if isinstance(self.image_2d,np.ndarray) is False:
            raise ValueError(' PSF provided could not be stored in an ndarray')

        if len(self.image_2d.shape)!=2:
            raise ValueError(' PSF provided is not a 2D image')

    def as_image(self, for_cube):
        #check for size
        if for_cube.shape[1:] != self.image_2d.shape:
            raise ValueError(' PSF Image and cube have different sizes: %s vs. %s' % (str(for_cube.shape[1:]),str(self.image_2d.shape)) )
        return self.image_2d

    def __str__(self):
        return """[PSF] :
  type = custom
  filename = {i.filename}""".format(i=self)


class GaussianPointSpreadFunction(PointSpreadFunction):
    """
    The default Gaussian Point Spread Function.

    fwhm: float
        Full Width Half Maximum in arcsec, aka. "seeing".
    pa: float [default is 0.]
        Position Angle of major-axis, anti-clockwise rotation from Y-axis, in angular degrees.
    ba: float [default is 1.0]
        Axis ratio of the ellipsis, b/a ratio (y/x).
    """
    def __init__(self, fwhm=None, pa=0, ba=1.0):
        self.fwhm = fwhm
        self.pa = pa
        self.ba = ba

    def __str__(self):
        return """[PSF] :
  type = Gaussian
  fwhm         = {i.fwhm} "
  pa           = {i.pa} °
  ba           = {i.ba}""".format(i=self)

    def as_image(self, for_cube, xo=None, yo=None):

        shape = for_cube.shape[1:]

        if xo is None:
            xo = (shape[1] - 1) / 2  #center of array
            #force PSF to be centered on even grid by adding 0.5pixel if even
            #because of the upcoming padding in the convolution
            xo = xo - (shape[1] % 2 - 1) /2
        if yo is None:
            yo = (shape[0] - 1) / 2  #center of array
            # force PSF to be centered on even grid by adding 0.5pixel if even
            # because of the upcoming padding in the convolution
            yo = yo - (shape[0] % 2 - 1) /2
        logger.info("Generating PSF at x0,y0 (%s,%s)" % (xo,yo))

        y, x = np.indices(shape)
        r = self._radius(xo, yo, x, y)
        fwhm = self.fwhm / for_cube.xy_step #in pixels

        psf = np.exp(-0.5 * (r / (fwhm / 2.35482)) ** 2)

        return psf / psf.sum()



class MoffatPointSpreadFunction(PointSpreadFunction):
    """
    The Moffat Point Spread Function

    fwhm if alpha is None: float [in arcsec]
        Moffat's distribution fwhm variable : http://en.wikipedia.org/wiki/Moffat_distribution
    alpha if fwhm is None: float [in arcsec]
        Moffat's distribution alpha variable : http://en.wikipedia.org/wiki/Moffat_distribution
    beta: float
        Moffat's distribution beta variable : http://en.wikipedia.org/wiki/Moffat_distribution

    pa: float [default is 0.]
        Position Angle of major-axis, the anti-clockwise rotation from Y,
        in angular degrees.
    ba: float [default is 1.0]
        Axis ratio of the ellipsis, b/a ratio (y/x).
    """

    def __init__(self, fwhm=None, alpha=None, beta=None, pa=0, ba=1):
        self.beta = beta
        self.pa = pa
        self.ba = ba
        self.alpha = alpha
        self.fwhm = fwhm

        if not ((alpha is None) or (fwhm is None)):
            self.logger.warning("Moffat psf: alpha and fwhm are both specified. Will use alpha. ")
        elif ((alpha is None) and (fwhm is None)):
            raise Error("Moffat psf: alpha and fwhm are not specified. Need at least one.")
        else:
            self.alpha = alpha
            self.fwhm = fwhm

        if fwhm is None:
            self.fwhm = self.calculate_fwhm()

        if alpha is None:
            self.alpha = self.calculate_alpha()

        if self.pa is None:
            raise Exception("Moffat error: please set P.A. 'pa'")
        if self.ba is None:
            raise Exception("Moffat error: please set axis ratio b/a 'ba'")
        if self.beta is None:
            raise Exception("Moffat error: please set beta parameter")

    def __str__(self):
        return """[PSF] :
  type = Moffat
  fwhm         = {i.fwhm} "
  alpha        = {i.alpha} "
  beta         = {i.beta}  
  pa           = {i.pa} °
  ba           = {i.ba}""".format(i=self)

    def as_image(self, for_cube, xo=None, yo=None):
       
        shape = for_cube.shape[1:]

        if xo is None:
            xo = (shape[1] - 1) / 2  #center of array
            #force PSF to be centered on even grid by adding 0.5pixel if even
            #because of the upcoming padding in the convolution
            xo = xo - (shape[1] % 2 - 1) /2
        if yo is None:
            yo = (shape[0] - 1) / 2  #center of array
            # force PSF to be centered on even grid by adding 0.5pixel if even
            # because of the upcoming padding in the convolution
            yo = yo - (shape[0] % 2 - 1) /2
        logger.info("Generating PSF at x0,y0 (%s,%s)" % (xo,yo))

        y, x = np.indices(shape)
        r = self._radius(xo, yo, x, y)

        pix_alpha = self.alpha / for_cube.xy_step

        psf = (1. + (r / pix_alpha) ** 2) ** (-self.beta)

        return psf / psf.sum()

    def calculate_fwhm(self):
        fwhm = self.alpha * (2. * np.sqrt(2. ** (1. / self.beta) - 1))
        return fwhm

    def calculate_alpha(self):
        alpha = self.fwhm / (2. * np.sqrt(2. ** (1. / self.beta) - 1))
        return alpha

if importlib.util.find_spec('maoppy') is not None:
    import maoppy
    RAD2ARCSEC = maoppy.utils.RAD2ARCSEC
    from maoppy.psfmodel import Psfao,  oversample
    from maoppy.psffit import psffit
    from maoppy.instrument import muse_nfm,muse_wfm
    from maoppy.utils import circavgplt,circavg
    logger.info("Found package Maoppy version {}".format(maoppy.__version__))

    class MAOPPYPointSpreadFunction(Psfao, PointSpreadFunction):
        """
        This class uses the MAOPPY PSF profile described by Fetick et al.
        (2019).

        References
        ----------
        Fetick et al. (2019, A&A, 628, A99)
           https://ui.adsabs.harvard.edu/abs/2019A&A...628A..99F/abstract

        """


        def __init__(self, r0=0.2, C=1e-7, amp=0.9, alpha=0.05, ba=1, pa=0,  beta=2.0, wvl_um=None, mode=None, Lext=10., fixed_k=None):
            """
            Initialize a new instance of the MAOPPY PSF.
            https://www.aanda.org/articles/aa/pdf/2019/08/aa35830-19.pdf

            Notes
            -----
            There are some differences in the parameter set of the MAOPPY PSF that
            is used by PampelMuse compared to the paper by Fetick et al. (2019).:

            1) The parameters C (the AO-corrected phase PSD background) and A (the
               residual variance) have been renamed to `C` and `amp`.

            2) Instead of defining two values for the effective radius of the
              Moffat, alpha_x and alpha_y, a single value `alpha` is used in
              combination with an ellipticity `e`.

            Parameters
            ----------

            r0 : float, optional
                The Fried parameter, given in units of [m].
            C : float, optional
                The AO-corrected phase PSD background, given in units of
                [m^2 rad^2].
            amp : float, optional
                The residual variance, given in units of [rad^2].
            alpha : float, optional
                The effective radius of the Moffat profile, given in units of
                [m^-1].
            ba : float, optional
                The  Moffat ellipticity
            pa: float, optional
                The  Moffat angle [degree]
            beta: float, optional
                The Moffat beta powerlaw
            wvl_um : float, optional
                The wavelength of the observation, given in units of [micron].
            mode: MUSE_WFM | MUSE_NFM
                [ no default ]

            Returns
            -------
            The newly defined instance.
            """

            # oversampling of the PSF on the PampelMuse level is not supported, because MAOPPY performs its
            # own oversampling when computing a PSF profile.


            # call initializer of parent class.
            #super(MAOPPYPointSpreadFunction, self).__init__(uc=uc, vc=vc, mag=mag, **kwargs)

            self.param_name_gpk = ['r0', 'C', 'amp', 'alpha', 'ba', 'theta', 'beta']
            #Maoppy Psfao
            #                    ["r0","bck","amp","alpha","ratio","theta","beta"]

            # initial parameter definitions
            self.r0 = r0
            self.C = C
            self.amp = amp
            self.alpha = alpha
            self.ba = ba
            self.pa = pa #in degrees
            self.theta = np.radians(pa) #in radians
            self.beta = beta
            self.flux = flux #in erg/s/cm2/AA
            self.mAB = mAB
            self.wvl_um = wvl_um
            self.mode = mode

            self.image_2d = None

            npix = (10, 10)  # will be modified in 'as_image'
            samp = 2.0  # will be modified in 'as_image'
            if mode == 'MUSE_WFM':
                system = muse_wfm
            elif mode == 'MUSE_NFM':
                system = muse_nfm
            else:
                raise ValueError('Maoppy Mode Not valid. Set mode to MUSE_WFM or MUSE_NFM')

            super().__init__(npix, system=system, lext=Lext, samp=samp, fixed_k=fixed_k)

            self.param = [self.r0, self.C, self.amp, self.alpha, self.ba, self.theta, self.beta]

        def __str__(self):
            return """[PSF] :
    type = Maoppy
    mode         = {i.mode}
    r0           = {i.r0} [m] 
    C            = {i.C} 
    amp          = {i.amp} [rad^2]
    fwhm         = {i.fwhm} "
    alpha        = {i.alpha} [m^-1]
    beta         = {i.beta}  
    pa           = {i.pa} °
    ba           = {i.ba}
    
    flux        = {i.flux} [erg/s/cm2/AA]
    mAB         = {i.mAB} 
    wvl_um      = {i.wvl_um} [micron]""".format(i=self)

        def set_p(self, p ):
            r0, C, A, alpha, ratio, theta, beta = p
            self.r0=r0
            self.C=C
            self.amp=A
            self.alpha=alpha
            self.beta=beta
            self.ba=ratio
            self.theta=theta
            self.pa=np.degrees(theta)

            self.param = [self.r0, self.C, self.amp, self.alpha, self.ba, self.theta, self.beta]

        def as_image(self, for_cube, xo=None, yo=None):
            """
            Return PSFAO as a 2D image shaped [for_cube].

            for_cube: HyperspectralCube
                Has additional properties computed and attributed by GalPaK :
                    - xy_step (in ")
                    - z_step (in µm) -> not used here...
                    - z_central (in µm)

            :rtype: ndarray
            """
            self.shape = self.npix = shape = for_cube.shape[1:]  ##must be npix for re-use by Maoppy
            if xo is None:
                xo = (shape[1] - 1) / 2  # center of array
                # force PSF to be centered on odd grid by adding 0.5pixel if even
                # because of the upcoming padding in the convolution
                xo = xo - (shape[1] % 2 - 1) / 2
            if yo is None:
                yo = (shape[0] - 1) / 2  # center of array
                # force PSF to be centered on odd grid by adding 0.5pixel if even
                # because of the upcoming padding in the convolution
                yo = yo - (shape[0] % 2 - 1) / 2
            self.logger.info("Generating PSF at x0,y0 (%s,%s)" % (xo, yo))

            self.center = (xo, yo)

            self.system._resolution_rad = for_cube.xy_step / RAD2ARCSEC
            if 'angstr' in for_cube.z_cunit.lower():
                wvl_um = for_cube.z_central / 1e4
            elif 'micron' in for_cube.z_cunit.lower():
                wvl_um = for_cube.z_central
            elif 'nm' in for_cube.z_cunit.lower():
                wvl_um = for_cube.z_central / 1e3
            else:
                raise NotImplementedError("Cube units not supported")

            self.samp = self.system.samp(wvl_um * 1e-6)
            if self.wvl_um is not None:
                self.logger.info("Computing PSF at {} from {}".format(wvl_um,self.wvl_um))
                ww = wvl_um/self.wvl_um # wavelength ratio
            else:
                ww = 1.0

            r0,C,A,alpha,ratio,theta,beta = self.param
            # see Fetick's papers
            p = [r0*ww**(6./5.),C*ww**(-2),A*ww**(-2),alpha,ratio,theta,beta]
            self.set_p(p)
            self.wvl_um = wvl_um

            dx = 0 #-(1 - self.shape[1] % 2) / 2
            dy = 0 #-(1 - self.shape[0] % 2) / 2

            self.image_2d =  self.__call__(p, dx=dx, dy=dy)
            return self.image_2d

        def calculate_fwhm(self):
            """
            Estimate and return the FWHM of the MAOPPY PSF profile for a given
            set of parameters.

            To estimate the FWHM, the method creates the MAOPPY PSF on a 2dim.
            grid, then determines the symmetric radial profile, and tries to
            obtain the radii where the intensity drops to half its central value
            using univariate spline interpolation.

           Returns
            -------
            fwhm : float
                The FWHM of the MAOPPY PSF for the given input parameters.
            """


            if self.image_2d is not None:
                psf = self.image_2d

                r, fr = circavgplt(psf)
                f = InterpolatedUnivariateSpline(r, fr - fr.max() / 2.) #why psf? should be fr
                roots = f.roots()

                if len(roots) != 2:
                    self.logger.error("Could not estimate FWHM of MAOPPY profile.")
                    return np.nan
                else:
                    return roots.max() - roots.min()
            else:
                return None

        @property
        def fwhm(self):
            """
            Returns
            -------
            fwhm : float
                The FWHM of the MAOPPY PSF profile with the given parameters.
            """
            fwhm = MAOPPYPointSpreadFunction.calculate_fwhm(self)
            if fwhm is not None:
                return fwhm * self.system._resolution_rad * RAD2ARCSEC
            else:
                return fwhm

        @property
        def strehl(self):
            """
            Returns
            -------
            strehl : float
                The Strehl ratio for the current set of parameters.
            """
            #psf = self.Psfao(npix=(30, 30), system=self.muse_nfm, samp=self.muse_nfm.samp(self.wvl))
            return self.strehlOTF((self.r0, self.C, self.amp, self.alpha,  self.ba, self.pa, self.beta))

            # Analytical calculation based on eq. 14 from the paper by Fetick et al. (2019). This seems to underestimate
            # the Strehl significantly for NFM data.
            # f_ao = muse_nfm.Nact/(2.*muse_nfm.D)
            # return np.exp(-self.amp - self.bck*np.pi*(f_ao**2) - (0.023*6.*np.pi*(self.r0*f_ao)**(-5./3.))/5.)

        def show_psf(self, filename=None):
            from matplotlib import pyplot as plt
            from matplotlib.colors import LogNorm

            if self.image_2d is not None:
                fig = plt.figure(1)
                plt.subplot(221)
                img=self.image_2d
                plt.imshow(img,norm=LogNorm())
                plt.title("PSF maoppy")

                plt.subplot(222)
                r,prof = circavgplt(self.image_2d)
                plt.semilogy(r,prof)
                plt.title("Profile ")

                plt.subplot(224)
                g=r>=0
                plt.loglog(r[g],prof[g])

                plt.subplot(223)
                psd,_=self.psd(self.param)
                plt.loglog(circavg(psd))
                plt.title("PSD")
                plt.xlabel('f [1/m]')

                if filename is not None:
                    fig.savefig(filename)

                return fig
            else:
                self.logger.error(" Maoppy PSF empty. Must run tthe method as_image(cube) before")

        def set_bounds(self, Model, bounds_dict):
            """

            :param bounds_dict: dictionnary of tuples
            :return:
            """
            #looping over parameters as defined in model Class
            for i,p in enumerate(self.param_name_gpk):
                #assumes parameters in same order!
                if p in bounds_dict.keys():
                    Model.bounds[0][i] = bounds_dict[p][0]
                    Model.bounds[1][i] = bounds_dict[p][1]

            return Model

        def fitter(self, psf_image,  parameters=['r0', 'amp', 'ba',  'theta'], weights=None, \
                   fit_background=True, positive_bck = False, guess=None, bounds_dict=None):
            """
            psf : 2D-sequence of floats
                The psfimage (2D)

            parameters : list of strings
                The names of the PSF parameters that should be optimized during
                the fit.
                default ['r0',  'amp', 'ba',  'theta']
                for AO use:  ['r0',  'amp', 'ba',  'theta', 'alpha', 'beta']
                for AO full :['r0',  'amp', 'ba',  'theta, ' alpha', 'beta', 'C']
                Mind that the other parameters are taken from self

            weights : 2D-sequence of floats
                The weights for the pixels on which the PSF profile is
                defined.

            fit_background : bool, optional
                Flag indicating if a constant background component should be
                included in the PSF fit.
            """
            from .convolution import padding
            psf_padded, boxpsf = padding(psf_image) #padding to even box size

            import collections
            FitResult = collections.namedtuple(
                'FitResult',
                ['names', 'x0', 'best_fit', 'errors', 'cost', 'flux', 'background', 'centroid', 'success', 'psf', 'residuals', 'message'])

            ron = self.system.ron

            if weights is None:
                weights = np.ones_like(psf_image) / ron**2
            weights, _ = padding(weights)

            #parameters to fit
            if parameters is None:
                parameters = self.param_name_gpk

            self.logger.info("MAOPPY PSF fit: setting up fitting with {:d} parameters {}".format(len(parameters),parameters))
            # %% Initialize PSF model
            samp = self.system.samp(self.wvl_um * 1e-6)  # sampling (2.0 for Shannon-Nyquist)

            self.logger.info("MAOPPY PSF fit: instanciation of Psfao")
            Pmodel = Psfao(psf_padded.shape, system=self.system, samp=samp)

            # define fixed parameters
            fixed = np.ones(len(self.param_name_gpk), dtype=bool)
            x0 = []

            for i, parameter in enumerate(self.param_name_gpk):
                if parameter in parameters:
                    fixed[i] = False
                # axis ratio is fitted instead of ellipticity
                if guess is None:
                    self.logger.info("MAOPPY: fitter: using initial x0 from self.parameters")
                    x0.append(getattr(self, parameter))
                else:
                    x0.append(guess[i])
            self.fixed=np.array(fixed)
            self.guess=np.array(x0)

            not_fitted = np.array(self.param_name_gpk)[self.fixed]
            self.logger.info("MAOPPY fit: parameters fixed: {}".format(not_fitted))

            if bounds_dict is not None:
                self.logger.info("MAOPPY fit: setting bounds with {}".format(bounds_dict))
                Pmodel = self.set_bounds(Pmodel, bounds_dict)

            # %% Fit the PSF with Psfao
            self.logger.info("MAOPPY fitting: mode = {}; option fit_background={} ".format(self.mode, fit_background ))
            fitresult = psffit(psf_padded, Pmodel, self.guess, weights=weights, fixed=self.fixed, \
                    flux_bck = (True, fit_background), positive_bck = positive_bck, npixfit = None )
            J = fitresult.jac
            cov = np.linalg.inv(J.T.dot(J))

            values={}
            errors={}
            _idx = (fixed==False).cumsum()
            for i, p in enumerate(self.param_name_gpk):
                if p in parameters:
                    values[p] = fitresult.x[self.param_name_gpk.index(p)]
                    _ii = _idx[self.param_name_gpk.index(p)]
                    errors[p] = np.sqrt(np.diagonal(cov))[_ii]
                elif fixed[i]==True:
                    values[p] = x0[i]
                    errors[p] = 0
                else:
                    raise Exception

            bestfit_model = fitresult.psf
            residuals_2d = psf_padded - fitresult.flux_bck[1] - fitresult.flux_bck[0] * bestfit_model

            cost = fitresult.cost

            x_center = psf_image.shape[1] // 2.
            y_center = psf_image.shape[0] // 2.

            # return fitresult

            #circularize theta
            values['theta'] = values['theta'] % (np.pi)
            errors['theta'] = errors['theta'] % (np.pi)

            if fitresult.success:
                centroid = (x_center + fitresult.dxdy[0] , y_center + fitresult.dxdy[1] )
                return FitResult(names=parameters,
                                 x0=guess,
                                 best_fit=values,
                                 errors=errors,
                                 cost=cost,
                                 flux=fitresult.flux_bck[0],
                                 background=fitresult.flux_bck[1] if fit_background else None,
                                 centroid=centroid,
                                 success=fitresult.success,
                                 residuals=residuals_2d[boxpsf],
                                 psf=bestfit_model[boxpsf],
                                 message=fitresult.message)
            else:
                return FitResult(names=parameters,
                                 x0=guess,
                                 best_fit=np.nan * np.ones_like(guess),
                                 errors=np.nan * np.ones_like(guess),
                                 flux=np.nan,
                                 cost=np.nan,
                                 background=np.nan if fit_background else None,
                                 centroid=(np.nan, np.nan),
                                 success=fitresult.success,
                                 residuals=None,
                                 psf=None,
                                 message=fitresult.message)
            #return fitresult
        def from_fitter(self,results):
            self.set_p(results.best_fit.values())
            self.image_2d = results.psf
            self.flux = results.flux * 1e-20 #erg/s/cm2/AA
            flux_Jy = 3.34e4 * (self.wvl_um*1e4) ** 2 * results.flux * 1e-20
            self.mAB = -2.5 * np.log10(flux_Jy / 3631.)



else:
    logger.warning('Package "maoppy" is not installed [not required]. Cannot use MAOPPY PSF model.')


## LINE SPREAD FUNCTIONS #######################################################


class LineSpreadFunction:
    """
    This is the interface all Line Spread Functions (LSF) should implement.
    """

    z_cunit = 'Undef'

    def as_vector(self, for_cube):
        """
        Should return this LSF as a 1D vector shaped [for_cube].

        for_cube: HyperspectralCube

        :rtype: ndarray
        """
        raise NotImplementedError()

class NoLineSpreadFunction(LineSpreadFunction):
    """
    A point spread function that does not spread anything, and returns the cube unchanged.
    Passing this to the instrument's lsf is the same as passing None.
    """
    def __init__(self):
        pass

    def as_vector(self, for_cube):
        """
        returns the identity LSF with ones
        :param for_cube:
        :return:
        """
        shape = for_cube.shape[0]
        return np.ones(shape)

    def __str__(self):
        return """[LSF] :\n  type = undefined """


class VectorLineSpreadFunction(LineSpreadFunction):
    """
    A custom line spread function using a provided 1D `vector`
    that should have the same length as the cube's (z).
    Should be centered around zo = (zsize - 1) / 2 - (zsize % 2 - 1)
    """

    def __init__(self, vector):
        self.vector = vector

    def as_vector(self, for_cube):
        return self.vector

    def __str__(self):
        return """[LSF] \n type = Custom """


class GaussianLineSpreadFunction(LineSpreadFunction):
    """
    A line spread function that spreads as a gaussian.
    We assume the centroid is in the middle.

    fwhm: float
        Full Width Half Maximum, in units of CUNIT3
    """
    def __init__(self, fwhm):
        self.fwhm = fwhm

    def __str__(self):
        return """[LSF] :
  type = Gaussian
  fwhm = {i.fwhm}  {i.z_cunit} \n""".format(i=self)

    def as_vector(self, for_cube):
        # Std deviation from FWHM
        sigma = self.fwhm / 2.35482 / for_cube.z_step
        # Resulting vector shape
        depth = for_cube.shape[0]
        # Assymmetric range around 0
        zo = (depth - 1) / 2 - (depth % 2 - 1) / 2
        z_range = np.arange(depth) - zo
        # Compute gaussian (we assume peak is at 0, ie. µ=0)
        lsf_1d = self.gaussian(z_range, 0, sigma)
        # Normalize and serve
        return lsf_1d / lsf_1d.sum()

    @staticmethod
    def gaussian(x, mu, sigma):
        """
        Non-normalized gaussian function.

        x : float|numpy.ndarray
            Input value(s)
        mu : float
            Position of the peak on the x-axis
        sigma : float
            Standard deviation

        :rtype: Float value(s) after transformation, of the same shape as input x.
        """
        return np.exp((x - mu) ** 2 / (-2. * sigma ** 2))


class MUSELineSpreadFunction(LineSpreadFunction):
    """
    A line spread function that uses MPDAF's LSF.
    See http://urania1.univ-lyon1.fr/mpdaf/chrome/site/DocCoreLib/user_manual_PSF.html

    .. warning::
        This requires the mpdaf module.
        Currently, the MPDAF module only works for odd arrays.
    model: string
        See ``mpdaf.MUSE.LSF``'s ``typ`` parameter.
    """
    def __init__(self, model="qsim_v1"):
        self.model = model
        try:
            from mpdaf.MUSE import LSF
        except ImportError:
            raise ImportError("You need the mpdaf module to use MUSELineSpreadFunction.")
        self.lsf = LSF(typ=self.model)


    def __str__(self):
        return """MUSE LSF : model = '{i.model}'""".format(i=self)

    def as_vector(self, cube):
        # Resulting vector shape
        depth = cube.shape[0]
        odd_depth = depth if depth % 2 == 1 else depth+1
        # Get LSF 1D from MPDAF
        if 'micron' in cube.z_cunit.lower():
            wavelength_aa = cube.z_central * 1e4  # unit conversion from microns to AA
            z_step_aa = cube.z_step * 1e4
        else:
            wavelength_aa = cube.z_central
            z_step_aa = cube.z_step

        lsf_1d = self.lsf.get_LSF(lbda=wavelength_aa, step=z_step_aa, size=odd_depth)

        x=np.arange(np.size(lsf_1d))
        sigma = np.sqrt(np.sum(x**2*lsf_1d)-np.sum(x*lsf_1d)**2) * cube.z_step

        self.fwhm = sigma * 2.35

        # That LSF is of an odd depth, truncate it if necessary
        # FIXME @nicolas : this is a hotfix, not really pretty, how can we do this better?
        if depth % 2 == 0:
            lsf_1d = lsf_1d[:-1]
        # Normalize and serve
        return lsf_1d / lsf_1d.sum()
