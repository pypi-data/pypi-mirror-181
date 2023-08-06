
import os
import configparser
from .spread_functions import  *
from .model_sersic3d import ModelSersic
from .instruments import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('GalPaK: Utils')

def _save_to_file(filename, contents, clobber):
    if not clobber and os.path.isfile(filename):
        raise IOError("The file {} already exists. Specify overwrite=True to overwrite it.".format(filename))
    with open(filename, 'w') as f:
        f.write(contents)

def _read_file(filename):
    with open(filename, 'r') as f:
        contents = f.read()
    return contents


def _read_psf(file_config=None):
    """
    set PSF from config file
    """
    psf = None
    if file_config is not None:
        if os.path.isfile(file_config):
            config = configparser.RawConfigParser()
            config.read(file_config)
        else:
            raise ValueError("PSF Config file %s not present! " % (file_config))
    else:
        raise ValueError("PSF Config file not defined")

    config = config['PSF']

    psf_keys={}
    for k in ['type', 'r0', 'C', 'amp', 'fwhm', 'alpha', 'beta', 'ba', 'pa', 'wvl_um', 'mode']:
        if k in config.keys():
            psf_keys[k] = k
        elif 'psf_'+k in config.keys():
            psf_keys[k] = 'psf_'+k

    if 'type' in psf_keys:
        psf_type = config[psf_keys['type']].lower()
        logger.info("CONFIG: PSF: type {%s} found " % (psf_type))
    else:
        logger.error("CONFIG: PSF: type not specified")



    if psf_type == 'moffat':
        psf = MoffatPointSpreadFunction
    elif psf_type == 'gaussian':
        psf = GaussianPointSpreadFunction
    elif psf_type == 'custom':
        psf = ImagePointSpreadFunction
    elif psf_type == 'maoppy':
        psf =  MAOPPYPointSpreadFunction
    else:
        #@fixme add other options
        raise NotImplementedError("Currently only PSF type = `moffat` and `gaussian` supported")
    args = {}
    import inspect
    var_args = inspect.getargspec(psf).args
    for k in var_args[1:]:
        if k in list(config.keys()):
            try:
                args[k] = eval(config[k].split()[0])
            except:
                args[k] = config[k]

    return psf(**args)

def _read_lsf(file_config=None):
    """
    sets LSF from config LSF: lsf_fwhm
    :return:
    """
    lsf = None
    if file_config is not None:
        if os.path.isfile(file_config):
            config =configparser.RawConfigParser()
            config.read(file_config)
        else:
            raise ValueError("LSF Config file %s not present! " % (file_config))
    else:
        raise ValueError("LSF Config file not defined")

    config = config['LSF']

    lsf_keys={}
    for k in ['type', 'fwhm']:
        if k in list(config.keys()):
            lsf_keys[k] = k
        elif 'lsf_'+k in config.keys():
            lsf_keys[k] = 'lsf_'+k

    if 'type' in lsf_keys:
        lsf_type = config[lsf_keys['type']].lower()
    else:
        lsf_type = None
        logger.warning("CONFIG: LSF: type not specified")

    if lsf_type == 'gaussian':
        lsf = GaussianLineSpreadFunction(
            fwhm=float(config[lsf_keys['fwhm']].split()[0])
        )  # lsf_fwhm,
    elif lsf_type is None:
        lsf = None
    else:
        #@fixme
        raise NotImplementedError

    return lsf

def _read_instrument(file_config):

    if file_config is not None:
        if os.path.isfile(file_config):
            config = configparser.RawConfigParser()
            config.read(file_config)
        else:
            raise ValueError("Instrument Config file %s not present! " % (file_config))
    else:
        raise ValueError("Instrument Config not defined")

    psf = _read_psf(file_config)
    try:
        lsf = _read_lsf(file_config)
    except:
        lsf = None
        logger.warning("CONFIG: LSF not found in config file")

    if 'INSTRUMENT' in config.sections():
        config = config['INSTRUMENT']
        myinstr = config['type'].lower()
        logger.info("CONFIG: INSTRUMENT: type {%s} found " % (myinstr))

        if 'pixscale' in list(config.keys()):
            scale = float(config['pixscale'].split()[0])  #
        else:
            scale = None

        if 'muse' == myinstr:
            instrument = MUSE(psf=psf, lsf=lsf)
        elif 'musewfm' == myinstr:
            instrument = MUSEWFM(psf=psf, lsf=lsf)
        elif 'musenfm' == myinstr:
            instrument = MUSENFM(psf=psf, lsf=lsf)
        elif 'alma' in myinstr:
            instrument = ALMA(psf=psf, lsf=lsf, pixscale=scale)
        elif 'sinfok250' in myinstr:
            instrument = SINFOK250(psf=psf, lsf=lsf)
        elif 'sinfok100' in myinstr:
            instrument = SINFOK100(psf=psf, lsf=lsf)
        elif 'sinfoj250' in myinstr:
            instrument = SINFOJ250(psf=psf, lsf=lsf)
        elif 'sinfoj100' in myinstr:
            instrument = SINFOJ100(psf=psf, lsf=lsf)
        elif 'harmoni' in myinstr:
            instrument = HARMONI(psf=psf, lsf=lsf, pixscale=scale)
        elif 'kmos' in myinstr:
            instrument = KMOS(psf=psf, lsf=lsf)
        elif 'osiris' in myinstr:
            instrument = OSIRIS(psf=psf, lsf=lsf)
        elif 'generic' in myinstr:
            instrument = Generic(psf=psf, lsf=lsf, default_spaxel_size=scale)
        else:
            # @fixme:generalize
            raise NotImplementedError
    else:
        #default
        logger.info("CONFIG: INSTRUMENT not present. Will use MUSE as default")
        instrument = MUSE(psf=psf, lsf=lsf)
    return instrument

def _read_model(file_config):
    """
    sets model from config MODEL
    :return:
    """

    model = None
    if file_config is not None:
        if os.path.isfile(file_config):
            logger.info("Reading model {:s}".format(file_config))
            config = configparser.RawConfigParser()
            config.read(file_config)
        else:
            raise ValueError("Model Config file %s not present" % (file_config))
    else:
        raise ValueErrror("Model Config file not defined")

    if config.has_section('MODEL'):
        config = config['MODEL']
    else:
        logger.warning("CONFIG file has no MODEL section")

    if 'type' in list(config.keys()):
        model_type = config['type'].lower()
    else:
        logger.error("CONFIG: Model: type not specified")


    args={}
    #try:
    #    redshift = float(config['redshift'])
    #except:
    #    redshift = None

    #args['redshift']=redshift

    if  'default' in model_type:
        model = DefaultModel
    elif 'sersic2d' in model_type:
        model = ModelSersic2D
    elif 'sersic' in model_type:
        model = ModelSersic
        if 'rotation_curve' in config.keys():
            args['rotation_curve']=config['rotation_curve']
    elif 'decomp' in model_type:
        model = ModelDecomp
    else:
        raise ValueError("Model type invalid. Must be ModelSersic2D or ModelSersic or ModelDecomp")

    #args parameters
    import inspect
    var_args = inspect.getargspec(model).args
    for k in var_args[1:]:
        if k.lower() in list(config.keys()):
            try:
                args[k]=eval(config[k])
            except:
                args[k]=config[k]


    return model(**args)
