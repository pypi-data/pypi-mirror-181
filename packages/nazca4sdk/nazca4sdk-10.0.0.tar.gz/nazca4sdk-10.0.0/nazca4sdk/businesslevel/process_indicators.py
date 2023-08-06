"""Module to calculate process indicators"""
from pydantic import ValidationError
from nazca4sdk.businesslevel.__brain_connection import BrainClient
from nazca4sdk.datahandling.variable_verificator import ProcessIndexParams, ProcessIndicatorParams


class ProcessIndicators():
    """ Class to perform process indicators calculation with cooperation with Brain """

    def __init__(self):
        self.indicators_brain = BrainClient()

    def calculate_cp_pp_indicator(self, cp_pp_input: dict):
        """
        Function to determine cp/pp indicator values for determined input

        Args:
            cp_pp_input: dictionary with input parameters:
                name: cp or pp indicator,
                lsl : lower specification limit,
                usl : upper specification limit,
                std: standard deviation

        Returns:
            cp/pp indicator

       """

        try:
            data = dict(ProcessIndicatorParams(**cp_pp_input))
            response = self.indicators_brain.get_cp_pp_indicator(data)
            result = self.indicators_brain.parse_response(response)
            if result is None:
                return None
            return result.to_df()
        except ValidationError as error:
            print(error.json())
            return None

    def calculate_cpk_ppk_indicator(self, cpk_ppk_input: dict):
        """
        Function to determine process performance index indicator values for determined input

        Args:
            cpk_ppk_input: dictionary with input parameters:
                lsl : lower specification limit,
                usl : upper specification limit,
                mean: mean value of samples,
                std: standard deviation


        Returns:
            cpk/ppk indicator

        """

        try:
            data = dict(ProcessIndexParams(**cpk_ppk_input))
            response = self.indicators_brain.get_cpk_ppk_indicator(data)
            result = self.indicators_brain.parse_response(response)
            if result is None:
                return None
            return result.to_df()
        except ValidationError as error:
            print(error.json())
            return None
