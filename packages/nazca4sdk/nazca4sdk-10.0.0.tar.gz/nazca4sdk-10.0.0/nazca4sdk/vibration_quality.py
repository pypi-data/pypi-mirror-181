"""Vibration quality module"""
from pydantic import ValidationError
from nazca4sdk.businesslevel.vibration_quality import VibrationQuality


def get_vibration_quality(group: str = 'G1r', vibration: float = 0):
    """
    Function to determine vibration quality values for determined input

    Args:
        group : Option for installation of machine according to ISO 10816
            possible: G1r, G1f,G2r, G2f,G3r, G3f,G4r, G4f ;
        vibration : Vibration value;

    Returns:
        DataFrame: vibration quality parameters with time response, cpu usage and ram usage

    Example:
        get_vibration_quality(group='G1r', vibration= 0)
    """

    try:
        vibration_quality = VibrationQuality()
        data = {"group": group,
                "vibration": vibration
                }
        result = vibration_quality.calculate_vibration_quality(data)
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
