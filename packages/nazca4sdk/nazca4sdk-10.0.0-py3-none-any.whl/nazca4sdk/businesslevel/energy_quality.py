"""Module to calculate energy quality according to EN50160"""
from pydantic import ValidationError
from nazca4sdk.businesslevel.__brain_connection import BrainClient
from nazca4sdk.datahandling.variable_verificator import EnergyInput


class EnergyQuality:
    """ Class to send and receive information from Energy quality module in brain"""

    def __init__(self):
        self.energy_brain = BrainClient()

    def calculate_energy_quality(self, input_energy: dict):
        """
        Function to determine energy quality values for determined input

        Args:
            ::input_energy -> dictionary with energy parameters::
        (
            freq1 : frequency value phase 1 (should be in range (0 - 60Hz));
            vol1 : voltage value phase 1 (should be in range (0 - 230V));
            cos1 : cosinus value phase 1 (should be in range (0 - 1));
            thd1 : thd value phase 1 (should be in range (0 - 10));
            freq2 : frequency value phase 2 (should be in range (0 - 60Hz));
            vol2 : voltage value phase 2 (should be in range (0 - 230V));
            cos2 : cosinus value phase 2 (should be in range (0 - 1));
            thd2 : thd value phase 2 (should be in range (0 - 10));
            freq3 : frequency value phase 3 (should be in range (0 - 60Hz));
            vol3 : voltage value phase 3 (should be in range (0 - 230V));
            cos3 : cosinus value phase 3 (should be in range (0 - 1));
            thd3 : thd value phase 3 (should be in range (0 - 10));
            standard : working norm type 1 - PN 50160;
        )
        Returns:
            ::energy quality parameters -> dictionary with energy quality parameters::
            (worstCaseQuality: Overall energy quality;
            worstCaseQuality1: Overall energy quality of phase 1;
            worstCaseQuality2 Overall energy quality of phase 2;
            worstCaseQuality3: Overall energy quality of phase 3;
            frequencyQuality1: Overall frequency quality of phase 1;
            voltageQuality1: Overall voltage quality of phase 1;
            cosQuality1: Overall cosinus quality of phase 1;
            thdQuality1: Overall thd quality of phase 1;
            frequencyQuality2: Overall frequency quality of phase 2;
            voltageQuality2: Overall voltage quality of phase 2;
            cosQuality2: Overall cosinus quality of phase 2;
            thdQuality2: Overall thd quality of phase 2;
            frequencyQuality3: Overall frequency quality of phase 3;
            voltageQuality3: Overall voltage quality of phase 3;
            cosQuality3: Overall cosinus quality of phase 3;
            thdQuality3: Overall thd quality of phase 3;
        """

        try:
            data = dict(EnergyInput(**input_energy))
            response = self.energy_brain.get_energy_quality(data)
            result = self.energy_brain.parse_response(response)
            if result is None:
                return None
            return result.to_df()
        except ValidationError as error:
            print(error.json())
            return None
