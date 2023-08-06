"""Energy Quality module"""
from dataclasses import dataclass
from pydantic import ValidationError
from nazca4sdk.businesslevel.energy_quality import EnergyQuality


@dataclass
class EnergyInfo:
    """Energy Info class

    Attributes:
    freq1 : frequency value phase 1;
    vol1 : voltage value phase 1;
    cos1 : cosinus value phase 1;
    thd1 : thd value phase 1;
    freq2 : frequency value phase 2;
    vol2 : voltage value phase 2;
    cos2 : cosinus value phase 2;
    thd2 : thd value phase 2;
    freq3 : frequency value phase 3;
    vol3 : voltage value phase 3;
    cos3 : cosinus value phase 3;
    thd3 : thd value phase 3;
    standard : working norm type 1 - PN 50160;

     """

    freq1: float = 0
    vol1: float = 230
    cos1: float = 1
    thd1: float = 0
    freq2: float = 50
    vol2: float = 230
    cos2: float = 1
    thd2: float = 0
    freq3: float = 50
    vol3: float = 230
    cos3: float = 1
    thd3: float = 0


def get_energy_quality(energy_info: EnergyInfo):
    """
    Function to determine energy quality values for determined input

    Args:
        energy_info: energy info


    Returns:
        DataFrame: energy quality parameters with time response, cpu usage and ram usage

    Example:
        get_energy_quality(freq1 = 50, vol1 = 230, cos1 = 1, thd1 = 0,
        freq2 = 50, vol2 = 230, cos2 = 1, thd2 = 0,
         freq3 = 50, vol3 = 230, cos3 = 1, thd3 = 0)
    """
    try:
        standard = 1
        energy_quality = EnergyQuality()
        data = {'freq1': energy_info.freq1,
                'vol1': energy_info.vol1,
                'cos1': energy_info.cos1,
                'thd1': energy_info.thd1,
                'freq2': energy_info.freq2,
                'vol2': energy_info.vol2,
                'cos2': energy_info.cos2,
                'thd2': energy_info.thd2,
                'freq3': energy_info.freq3,
                'vol3': energy_info.vol3,
                'cos3': energy_info.cos3,
                'thd3': energy_info.thd3,
                'standard': standard
                }
        result = energy_quality.calculate_energy_quality(data)
        res = result.iloc[:, :-3]
        time_response = round(result.iloc[0, -3], 2)
        cpu_usage = result.iloc[0, -2]
        ram_usage = result.iloc[0, -1]
        if result is None:
            return None
        return res, time_response, cpu_usage, ram_usage
    except ValidationError as error:
        print(error.json())
        return None
