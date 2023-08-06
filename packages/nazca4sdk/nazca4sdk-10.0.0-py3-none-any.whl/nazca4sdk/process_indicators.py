"""Process indicators module"""
from pandas import DataFrame
import pandas as pd
import numpy as np
from pydantic import ValidationError
from nazca4sdk.businesslevel.process_indicators import ProcessIndicators



d2 = [1.128, 1.1693, 2.059, 2.326, 2.534, 2.704, 2.847, 2.970, 3.078, 3.173, 3.259, 3.336, 3.407, 3.472, 3.532, 3.588, 3.64, 3.689, 3.735,
      3.778,  3.819, 3.858, 3.895,  3.931,  3.964,  3.997, 4.027, 4.057, 4.086]


def __estimate_std_using_time(samples, offset, count):
    """
    The function to estimate standard deviation for Cp/Cpk indicator using time offset

    Args:
        samples: DataFrame with samples
        offset: time offset in seconds
        count: number of samples in subgroups

    Return:
        estimated standard deviation
    """
    ranges = []
    start = samples.head(1).measureTime
    time = start

    while time.values < samples.tail(1).measureTime.values:
        data = (samples[samples['measureTime'].values >
                time.values].iloc[0:count])
        if data.shape[0] == count:
            ranges.append(max(data.value)-min(data.value))
        time = time + pd.DateOffset(seconds=offset)
    return np.mean(ranges)/d2[count-2]


def __estimate_std_using_samples(samples, offset, count):
    """
    The function to estimate standard deviation for Cp/Cpk indicator using samples offset

    Args:
        samples: DataFrame with samples
        offset: number of samples between subgroups
        count: number of samples in subgroups

    Return:
        estimated standard deviation
    """
    ranges = []
    idx = samples.index[0]
    while idx < samples.index[-1]:
        data = (samples.iloc[idx:idx+count])
        if data.shape[0] == count:
            ranges.append(max(data.value)-min(data.value))
        idx = idx+offset
    return np.mean(ranges)/d2[count-2]


def get_cp_indicator(lsl: float, usl: float, period: int, subgroups: int, samples: DataFrame, estimation_type='samples'):
    """
    The function to calculate Process Capability Indicator (Cp):

    Cp indicator is calculated as:

        Cp = (USL-LSL)/(6*std)
    Args:
        lsl : lower specification limit,
        usl : upper specification limit,
        period: when estimation_type = 'samples', this is number of samples, for estimation_type = 'time' this is number of seconds
        subgroups: number of samples in subgroups,
        samples: DataFrame with samples,
        estimation_type: 'time' to estimate std using time offset or 'samples' to estimate using number of samples offset

    Return:
        Cp value

    """
    try:
        indicators = ProcessIndicators()
        if estimation_type == 'samples':
            std = __estimate_std_using_samples(samples, period, subgroups)
        elif estimation_type == 'time':
            std = __estimate_std_using_time(samples, period, subgroups)
        else:
            raise ValueError(
                "Invalid estimation type. Expected 'time' or 'samples'")

        data = {"name": 'Cp',
                "lsl": lsl,
                "usl": usl,
                "std": std
                }

        result = indicators.calculate_cp_pp_indicator(data)
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None


def get_pp_indicator(lsl: float, usl: float, samples: DataFrame):
    """
    The function to calculate Process Performance Indicator (Pp):

    Pp indicator is calculated as:

        Pp = (USL-LSL)/(6*std)
    Args:
        lsl : lower specification limit,
        usl : upper specification limit,
        samples: DataFrame with samples

    Return:
        Pp value

    """
    try:
        indicators = ProcessIndicators()
        std = samples.value.std()
        data = {"name": 'Pp',
                "lsl": lsl,
                "usl": usl,
                "std": std
                }
        result = indicators.calculate_cp_pp_indicator(data)
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None


def get_cpk_indicator(lsl: float, usl: float, period: float, subgroups: int, samples: DataFrame):
    """
    The function to calculate Process Capability Index (Cpk):

    Cpk indicator is calculated as:

        Cpk = min(upper, lower)

        where:
            upper = (USL - mean)/(3*std)
            lower = (mean - LSL)/(3*std)

    Args:
        lsl: lower specification limit,
        usl: upper specification limit,
        period: number of samples between subgroups,
        subgroups: number of samples in subgroups,
        samples: DataFrame with samples

    Return:
        Pp value: float
    """
    try:
        indicators = ProcessIndicators()
        std = __estimate_std_using_samples(samples, period, subgroups)
        mean = samples.value.mean()
        data = {"name": 'Cpk',
                "lsl": lsl,
                "usl": usl,
                "mean": mean,
                "std": std
                }
        result = indicators.calculate_cpk_ppk_indicator(data)
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None


def get_ppk_indicator(lsl: float, usl: float, samples: DataFrame):
    """
    The function to calculate Process Performance Index (Ppk):

    Ppk indicator is calculated as:

        Ppk = min(upper, lower)

        where:
            upper = (USL - mean)/(3*std)
            lower = (mean - LSL)/(3*std)

    Args:
        lsl : lower specification limit,
        usl : upper specification limit,
        samples: DataFrame with samples

    Return:
        Ppk value

    """
    try:
        indicators = ProcessIndicators()
        std = samples.value.std()
        mean = samples.value.mean()
        data = {"name": 'Ppk',
                "lsl": lsl,
                "usl": usl,
                "mean": mean,
                "std": std
                }
        result = indicators.calculate_cpk_ppk_indicator(data)
        if result is None:
            return None
        return result
    except ValidationError as error:
        print(error.json())
        return None
