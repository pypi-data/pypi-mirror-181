"""
Daniell averaging method for CSD.

An upgrade to Pooya Saffarieh's, and Sam Scherf's asd2 port to Python.
This attemts to adress the following main issue, make 'csd_daniell' look like
'scipy.signal.csd' - with the goal of adding 'csd_daniell' to the
'scipy.signal' toolbox. This should offload the code maintanence to a
community with sufficient time and skill to do this.

Addresses:
 > Kwarg pass through.
 > Axes.
 > CSD vs ASD, CSD is ALWAYS more versatile.
 > Harmonising with Scipy Library.

Sources:
 > https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.csd.html
 > https://github.com/scipy/scipy/blob/v1.8.0/scipy/signal/_spectral_py.py
   #L454-L603
 > https://github.com/scipy/scipy/blob/v1.8.0/scipy/signal/_spectral_py.py
   #L1579-L1869
 > https://gitlab.nikhef.nl/6d/6dscripts/-/blob/master/SpectralAnalyzer/asd2.py
 > https://git.ligo.org/sam.scherf/ftools/-/blob/master/ftools/daniell.py
 > https://git.ligo.org/sam.scherf/ftools/-/blob/master/ftools/_utils.py


Authors: Nathan A. Holland, Pooya Saffarieh, Abhinav Petra, Conor Mow-Lowry
Associated Authors: Sam Scherf
Contact: nholland@nikhef.nl
Date: 2022-04-12

Modified for Spicypy by Artem Basalaev
Date: 2022-06-24
"""

from warnings import warn

import numpy as np
from gwpy.signal.spectral._utils import scale_timeseries_unit
from scipy.fft import fftshift, ifftshift  # pylint: disable=no-name-in-module
from scipy.signal import csd

from spicypy.signal.frequency_series import FrequencySeries


def daniell(*args, **kwargs):  # pylint: disable=too-many-branches
    """Calculate the CSD of a `TimeSeries` using Daniell's method
    Frequency domain averaging of the CSD.
    Parameters
    ----------
    args : `list`
        timeseries: `TimeSeries`
            input time series (if only one specified, calculates PSD)
        other: `TimeSeries`, optional
            second input time series
        nfft: `int`
            number of samples per FFT, only value equal to full time series length is accepted
    kwargs : `dict`
        fftlength : `float`, optional
            number of seconds in single FFT. User-specified value ignored,
            algorithm uses full duration.
        overlap : `float`, optional
            number of seconds of overlap between FFTs. User-specified value ignored,
            algorithm uses no overlap.
        window : `str`, `numpy.ndarray`, optional
            Window function to apply to timeseries prior to FFT.
            See :func:`scipy.signal.get_window` for details on acceptable formats. Defaults to 'hann'.
        additional arguments, passed to scipy.signal.CSD
    Returns
    -------
    fs: `FrequencySeries`
        resulting CSD
    """

    try:
        timeseries, nfft = args
        other = timeseries
    except ValueError:
        timeseries, other, nfft = args

    # Convert the inputs to numpy arrays.
    x = np.asarray(timeseries.value)
    y = np.asarray(other.value)

    if len(x) != len(y):
        raise ValueError("Time series must have the same length (number of samples)!")

    # No overlap for Daniell method.
    overlap = kwargs.pop("overlap", 0)
    if overlap is not None and overlap != 0:
        raise ValueError(
            "overlap argument is not supported by Daniell averaging method; "
            "single FFT covering the full duration is calculated, with averaging performed in frequency domain."
        )
    # noverlap is specified by GWpy by default, get rid of it
    kwargs.pop("noverlap")
    # and set noverlap to 0
    noverlap = 0

    # No fftlength for Daniell method.
    if kwargs.get("fftlength") or nfft != len(x):
        raise ValueError(
            "fftlength/nfft arguments are not supported by Daniell averaging method; "
            "single FFT covering the full duration is calculated, with averaging performed in frequency domain."
        )
    nperseg = len(x) + kwargs.pop("pad_length", 0)
    nfft = int(nperseg)

    # get window function
    window = kwargs.pop("window_", None)
    window = "hann" if window is None else window
    # clean up default value from kwargs
    if "window" in kwargs:
        kwargs.pop("window")
    if not isinstance(window, str):
        warn(
            "Specifying window as an array for Daniell averaging method is not supported, defaulting to 'hann' window"
        )
        window = "hann"

    # For now REQUIRES an odd number of averages, to handle complex
    # data types.
    number_averages = kwargs.pop("number_averages", 9)
    if (number_averages % 2) == 0:
        err = (
            f"Only an odd number of averages, not {number_averages} are "
            + "implemented - for complex symmetry reasons."
        )
        raise NotImplementedError(err)

    if number_averages < 1:
        err = f"Number of averages {number_averages} < 1 is nonsense."
        raise ValueError(err)

    # Check the averaging method.
    average = kwargs.pop("average", "mean")
    bias_correction = 1
    if average == "mean":
        avg_func = np.mean
    elif average == "median":
        # bias correction from _median_bias in Scipy 1.8
        ii_2 = 2 * np.arange(1.0, (number_averages - 1) // 2 + 1)
        bias_correction = 1 + np.sum(1.0 / (ii_2 + 1) - 1.0 / ii_2)
        avg_func = np.median
    else:
        err = (
            "Available options for <average> are 'mean' and 'median'"
            + f" not {average}."
        )
        raise ValueError(err)

    # Take the CSD.
    # Averaging isn't done by 'csd'.
    # In general the frequency vector has the ordering:
    #  0, f_positive, f_negative

    frq, _CSD = csd(
        x,
        y,
        fs=timeseries.sample_rate.decompose().value,
        window=window,
        nperseg=nperseg,
        noverlap=noverlap,
        nfft=nfft,
        **kwargs,
    )
    # scipy returns complex values with zero imaginary part... cast it to real
    if not np.iscomplex(_CSD).any():
        _CSD = np.real(_CSD)

    # Perform Daniell's averaging.

    # Check if it is onesided, actual not requested.
    is_onesided = not np.any(np.less(frq, 0))

    # Branch behaviour based upon if it is one or two sided.
    # TODO: FIX when slices end at -0
    if is_onesided:
        f, CSD = _daniell_one_sided(frq, _CSD, number_averages, avg_func)
    else:
        f, CSD = _daniell_two_sided(frq, _CSD, number_averages, avg_func)

    # Correct for bias.
    CSD /= bias_correction

    # generate FrequencySeries and return
    unit = scale_timeseries_unit(
        timeseries.unit,
        kwargs.pop("scaling", "density"),
    )
    fs = FrequencySeries(
        CSD,
        unit=unit,
        frequencies=f,
        name=timeseries.name,
        epoch=timeseries.epoch,
        channel=timeseries.channel,
    )

    return fs


def _daniell_one_sided(frq, _CSD, number_averages, avg_func):
    """Part of Daniell's method for real-valued CSD (one-sided)
    Parameters
    ----------
    frq : ndarray
        frequencies
    _CSD : ndarray
        CSD values at each frequency
    number_averages: int
        integer number of averages, must be odd
    avg_func: numpy.core.fromnumeric
        numpy function used for averaging, mean or median
    Returns
    -------
    f :  ndarray
        frequencies
    CSD: ndarray
        CSD values at each frequency
    """
    # Number of points for the DC bin.
    DC_points = number_averages // 2 + 1

    # Points to drop.
    end_drop = -1 * (frq[DC_points:].size % number_averages)
    if end_drop == 0:
        end_drop = None

    # Frequency vector.
    # Median is clearer than mean.
    f = np.median(frq[DC_points:end_drop].reshape((-1, number_averages)), axis=-1)
    f = np.insert(f, 0, 0.0)
    del frq

    # CSD.
    new_shape = (*_CSD.shape[:-1], -1, number_averages)
    __CSD = _CSD[..., DC_points:end_drop].reshape(new_shape)

    if np.iscomplexobj(__CSD):
        # Unnecessary for mean but results in no change.
        # No RMS because this is already squared.
        CSD = avg_func(__CSD.real, axis=-1) + 1j * avg_func(__CSD.imag, axis=-1)
        CSD = np.insert(
            CSD,
            0,
            avg_func(_CSD[..., :DC_points].real, axis=-1)
            + 1j * avg_func(_CSD[..., :DC_points].imag, axis=-1),
            axis=-1,
        )
    else:
        # Easy for real valued.
        CSD = avg_func(__CSD, axis=-1)
        CSD = np.insert(CSD, 0, avg_func(_CSD[..., :DC_points], axis=-1), axis=-1)
    del _CSD, __CSD

    return f, CSD


def _daniell_two_sided(frq, _CSD, number_averages, avg_func):
    """Part of Daniell's method for complex-valued CSD (one-sided)
    Parameters
    ----------
    frq : ndarray
        frequencies
    _CSD : ndarray
        CSD values at each frequency
    number_averages: int
        integer number of averages, must be odd
    avg_func: numpy.core.fromnumeric
        numpy function used for averaging, mean or median
    Returns
    -------
    f :  ndarray
        frequencies
    CSD: ndarray
        CSD values at each frequency
    """
    # Reorder the FFT.
    frq = fftshift(frq)
    _CSD = fftshift(_CSD, axes=-1)

    # Deal with even case.
    if (frq.size % 2) == 0:
        # Cut off the lowest frequency point, which has no
        # symmetric, positive counter part.
        frq = frq[1:]
        _CSD = _CSD[..., 1:]

    # Determine the number of points to drop.
    total_to_drop = frq.size % number_averages

    end_drop = -1 * (total_to_drop // 2)
    if end_drop == 0:
        end_drop = None

    start_drop = total_to_drop // 2
    if (total_to_drop % 2) != 0:
        # Need to drop the lowest frequency point too.
        start_drop += 1

    # Mean also works but median is clearer.
    f = np.median(frq[start_drop:end_drop].reshape((-1, number_averages)), axis=-1)
    del frq
    f = ifftshift(f)

    # Make the CSD.
    new_shape = (*_CSD.shape[:-1], -1, number_averages)
    _CSD = _CSD[..., start_drop:end_drop].reshape(new_shape)

    if np.iscomplexobj(_CSD):
        # Unnecessary for mean but results in no change.
        # No RMS because this is already squared.
        CSD = avg_func(_CSD.real, axis=-1) + 1j * avg_func(_CSD.imag, axis=-1)
    else:
        # Easy for real valued.
        CSD = avg_func(_CSD, axis=-1)
    del _CSD

    CSD = ifftshift(CSD, axes=-1)
    return f, CSD
