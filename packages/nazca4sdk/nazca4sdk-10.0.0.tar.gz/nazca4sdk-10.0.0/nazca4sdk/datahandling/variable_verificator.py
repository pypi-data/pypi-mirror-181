"""Variable verification module"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


class VariableIntervalInfo(BaseModel):
    """Class to verify the correctness of data for variable over time range
    when start and end date is set

    Attributes:
        module parameters: dict
    """
    module_name: str
    variable_names: list
    start_date: str
    end_date: str

    @validator('start_date')
    def start_date_verify_format(cls, valid_start_date):
        """Validator to check if time amount is correct

        Args:
            valid_start_date: str

        Returns:
            valid_start_date: str
        """
        return VariableIntervalInfo.valid_datetime(valid_start_date)

    @validator('end_date')
    def end_date_verify_format(cls, valid_end_date, values):
        """Validator to check if time amount is correct

        Args:
            valid_end_date: str
            values : str
        Returns:
            valid_end_date: str
        """
        VariableIntervalInfo.valid_datetime(valid_end_date)
        if 'start_date' in values:
            start_date_str = values['start_date']
            end_date = datetime.strptime(valid_end_date, DATE_TIME_FORMAT)
            start_date = datetime.strptime(start_date_str, DATE_TIME_FORMAT)
            if end_date > start_date:
                return valid_end_date
            raise ValueError(
                f'{valid_end_date} must be after {start_date_str}')
        raise ValueError('Cannot check if end_date is after start_date')

    @staticmethod
    def valid_datetime(valid_datetime):
        """Validator to check if time amount is correct

        Args:
            valid_datetime: str

        Returns:
            valid_datetime: str
        """
        try:
            datetime.strptime(valid_datetime, DATE_TIME_FORMAT)
            return valid_datetime
        except ValueError:
            raise ValueError(
                'Bad datetime format. Format yyyy-mm-ddTHH:MM:SS')


class VariableIntervalSubtractionInfo(BaseModel):
    """Class to verify the correctness of data for variable over time range
     when time unit and time amount is set

    Attributes:
        module parameters: dict
    """
    module_name: str
    variable_names: list
    time_unit: str

    time_amount: int

    @validator('time_amount')
    def time_amount_validator(cls, valid_time_amount):
        """
        Validator to check if time amount is correct

        Args:
            valid_time_amount: int

        Returns:
            valid_time_amount: int
        """
        if valid_time_amount <= 0:
            raise ValueError('time_amount has to be greater than 0')
        return valid_time_amount

    @validator('time_unit')
    def time_unit_validator(cls, valid_time_unit):
        """Validator to check if time unit is correct

        Args:
            valid_time_unit: str

        Returns:
            valid_time_unit: str
        """
        possibilities = ['SECOND', 'MINUTE', 'HOUR', 'DAY', 'WEEK', 'YEAR']
        if valid_time_unit not in possibilities:
            raise ValueError(
                'Wrong time aggregator, try: SECOND, MINUTE, HOUR, DAY, WEEK, YEAR')
        return valid_time_unit


class EnergyInput(BaseModel):
    """Class to verify the correctness of data for Energy Quality function

    Class to verify the correctness of data for Energy Quality function to energy input parameters
    to determine energy quality assessment according to norm: PN 50160

    Attributes:
    freq1: (float) frequency value phase 1;
    vol1: (float) voltage value phase 1;
    cos1: (float) cosinous value phase 1;
    thd1: (float) thd value phase 1;
    freq2: (float) frequency value phase 2;
    vol2: (float) voltage value phase 2;
    cos2: (float) cosinus value phase 2;
    thd2: (float) thd value phase 2;
    freq3: (float) frequency value phase 3;
    vol3: (float) voltage value phase 3;
    cos3: (float) cosinus value phase 3;
    thd3: (float) thd value phase 3;
    standard: (int) working norm type 1 - PN 50160;
    """
    freq1: float
    vol1: float
    cos1: float
    thd1: float
    freq2: float
    vol2: float
    cos2: float
    thd2: float
    freq3: float
    vol3: float
    cos3: float
    thd3: float
    standard: int

    @validator('freq1')
    def freq1_validate(cls, valid_freq1):
        """ Validator to check if frequency of phase 1 is correct"""

        if valid_freq1 <= 0:
            raise ValueError('Frequency of phase 1 has to be greater than 0')
        return valid_freq1

    @validator('freq2')
    def freq2_validate(cls, valid_freq2):
        """Validator to check if frequency of phase 2 is correct"""

        if valid_freq2 <= 0:
            raise ValueError('Frequency of phase 2 has to be greater than 0')
        return valid_freq2

    @validator('freq3')
    def freq3_validate(cls, valid_freq3):
        """ Validator to check if frequency of phase 3 is correct"""

        if valid_freq3 <= 0:
            raise ValueError('Frequency of phase 3 has to be greater than 0')
        return valid_freq3

    @validator('vol1')
    def vol1_validate(cls, valid_vol1):
        """Validator to check if voltage of phase 1 is correct"""

        if valid_vol1 <= 0:
            raise ValueError('Voltage V1 has to be greater than 0')
        return valid_vol1

    @validator('vol2')
    def vol2_validate(cls, valid_vol2):
        """ Validator to check if voltage of phase 2 is correct"""

        if valid_vol2 <= 0:
            raise ValueError('Voltage V2 has to be greater than 0')
        return valid_vol2

    @validator('vol3')
    def vol3_validate(cls, valid_vol3):
        """Validator to check if voltage of phase 3 is correct"""

        if valid_vol3 <= 0:
            raise ValueError('Voltage V3 has to be greater than 0')
        return valid_vol3

    @validator('cos1')
    def cos1_validate(cls, valid_cos1):
        """Cos 1 validator"""

        if valid_cos1 < 0:
            raise ValueError('Cos value of phase 1 is lower than zero, '
                             'check connection of a circuit')
        if valid_cos1 > 1.1:
            raise ValueError('Cos phase 1 is out of range')
        return float(valid_cos1)

    @validator('cos2')
    def cos2_validate(cls, valid_cos2):
        """Cos 2 validator"""

        if valid_cos2 < 0:
            raise ValueError('Cos value of phase 2 is lower than zero, '
                             'check connection of a circuit')
        if valid_cos2 > 1.1:
            raise ValueError('Cos phase 2 is out of range')
        return float(valid_cos2)

    @validator('cos3')
    def cos3_validate(cls, valid_cos3):
        """ Cos 3 validator"""

        if valid_cos3 < 0:
            raise ValueError('Cos value of phase 3 is lower than zero, '
                             'check connection of a circuit')
        if valid_cos3 > 1.1:
            raise ValueError('Cos phase 3 is out of range')
        return float(valid_cos3)

    @validator('thd1')
    def thd1_validate(cls, valid_thd1):
        """ THD 1 validator"""

        if valid_thd1 < 0 or valid_thd1 > 10:
            raise ValueError('THD phase 1 is out of range')
        return float(valid_thd1)

    @validator('thd2')
    def thd2_validate(cls, valid_thd2):
        """ THD 2 validator"""

        if valid_thd2 < 0 or valid_thd2 > 10:
            raise ValueError('THD phase 2 is out of range')
        return float(valid_thd2)

    @validator('thd3')
    def thd3_validate(cls, valid_thd3):
        """ THD 3 validator"""

        if valid_thd3 < 0 or valid_thd3 > 10:
            raise ValueError('THD phase 3 is out of range')
        return float(valid_thd3)


class VibrationInput(BaseModel):
    """Class to verify the correctness of data for Vibration Quality function

    Attributes:
    group : (str)  Option for installation of machine according to ISO 10816
        possible: G1r, G1f,G2r, G2f,G3r, G3f,G4r, G4f
    vibration : (float) Vibration value;

    """
    group: str
    vibration: float

    @validator('group')
    def group_validate(cls, group):
        """Validator to verify group input parameter"""

        option = ["G1r", "G1f", "G2r", "G2f", "G3r", "G3f", "G4r", "G4f"]
        if group not in option:
            raise ValueError('group name is specified in documentation, '
                             'should be: G1r, G1f,G2r, G2f,G3r, G3f,G4r, G4f')
        return group

    @validator('vibration')
    def vibration_validate(cls, vibration):
        """Validator to verify vibration input parameter"""

        v_max = 11  # Maximum vrms value according to ISO 10816
        v_min = 0  # Minimum vrms value according to ISO 10816
        if (vibration < v_min) or (vibration > v_max):
            raise ValueError('Vibration has to be in range 0 - 11')
        return float(vibration)


class OeeSimpleParams(BaseModel):
    """Class to verify the correctness of data for Simple OEE function

    Attributes:
    availability: float
    performance: float
    quality: float
    """
    availability: float
    performance: float
    quality: float

    @validator('availability')
    def availability_validator(cls, value):
        """ Availability parameter validator """
        if value < 0:
            raise ValueError('Availability has to be higher than')
        return float(value)

    @validator('performance')
    def performance_validator(cls, value):
        """ Performance parameter validator """
        if value < 0:
            raise ValueError('Performance has to be higher than')
        return float(value)

    @validator('quality')
    def quality_validator(cls, value):
        """Quality parameter validator """
        if value < 0:
            raise ValueError('Quality has to be higher than')
        return float(value)


class OeeComplexParams(BaseModel):
    """Class to verify the correctness of data for variable OEE

    Attributes:
    A : (float) Total available time,
    B : (float) Run time,
    C : (float) Production capacity,
    D : (float) Actual production,
    E : (float) Production output (same as actual production),
    F : (float) Actual good products (i.e. product output minus scraps)
    """

    A: float
    B: float
    C: float
    D: float
    E: float
    F: float


class AvailabilityValidator(BaseModel):
    """Class to verify the correctness of data for availability

    Attributes:
    run_time: float
    total_time: float
    """
    run_time: float
    total_time: float


class PerformanceValidator(BaseModel):
    """Class to verify the correctness of data for performance

    Attributes:
    actual_production: float
    production_capacity: float
    """
    actual_production: float
    production_capacity: float


class QualityValidator(BaseModel):
    """Class to verify the correctness of data for quality

    Attributes:
    actual_products: float
    production_output: float
    """
    actual_products: float
    production_output: float


class ProcessIndicatorParams(BaseModel):
    """
    Class to verify the correctness of data for process performance function

    Args:
    name : (str)
    lsl : (float)
    usl: (float)
    std : (float)

    """
    name: str
    lsl: float
    usl: float
    std: float

    @validator('name')
    def name_validate(cls, name):
        """ Cp/pp name validator """
        if name != 'Cp' and name != 'Pp':
            raise ValueError('Name has to be Cp or Pp')

        return name

    @validator('std')
    def std_validate(cls, std):
        """ Cp/pp std validator """
        if std == 0:
            raise ValueError('Value cannot be 0')

        return float(std)

    @validator('usl')
    def limits_validate(cls, usl, values):
        """ Cp/pp limits validator """

        lsl_value = values['lsl']

        if usl > lsl_value:
            return usl
        raise ValueError('Value has to be grater than lsl')


class ProcessIndexParams(BaseModel):
    """
    Class to verify the correctness of data for process performance function

    Attributes:
    name : (str)
    lsl : (float)
    usl : (float)
    mean : (float)
    std : (float)

    """
    name: str
    lsl: Optional[float]
    usl: Optional[float]
    mean: float
    std: float

    @validator('name')
    def name_validate(cls, name):
        """ Cpk/ppk name validator """
        if name != 'Cpk' and name != 'Ppk':
            raise ValueError('Name has to be Cpk or Ppk')

        return name

    @validator('std')
    def std_validate(cls, std):
        """ Cpk/ppk std validator """
        if std == 0:
            raise ValueError('Value cannot be 0')

        return float(std)

    @validator('usl', pre=True, always=True, whole=True)
    def limits_validate(cls, usl, values):
        """ Cpk/ppk limits validator """
        if not values.get('lsl') and not usl:
            raise ValueError('Either lsl or usl is required')

        if not usl:
            return

        if 'lsl' in values:
            lsl_value = values['lsl']

            if lsl_value is None:
                return usl
            if usl > lsl_value:
                return usl
            raise ValueError('Value has to be grater than lsl')
