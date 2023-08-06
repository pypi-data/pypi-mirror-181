"""Module to calculate vibration quality"""
from pydantic import ValidationError
from nazca4sdk.businesslevel.__brain_connection import BrainClient
from nazca4sdk.datahandling.variable_verificator import VibrationInput


class VibrationQuality:
    """ Class to send and receive information from Vibration quality module in brain"""

    def __init__(self):
        self.vibration_brain = BrainClient()

    def calculate_vibration_quality(self, input_vibro: dict):
        """Function to determine vibration quality values for determined input

        Args:
            ::input -> dictionary with vibration parameters::
        (
            group : Option for installation of machine according to ISO 10816
                possible: G1r, G1f,G2r, G2f,G3r, G3f,G4r, G4f ;
            vibration : Vibration value
        )

        Returns:
            dict: vibration quality parameters
        """

        try:
            data = dict(VibrationInput(**input_vibro))
            response = self.vibration_brain.get_vibration_quality(data)
            result = self.vibration_brain.parse_response(response)
            if result is None:
                return None
            return result.to_df()
        except ValidationError as error:
            print(error.json())
            return None
