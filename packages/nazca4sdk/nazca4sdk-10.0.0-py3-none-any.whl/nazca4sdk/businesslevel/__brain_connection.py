""" Module to communicate with Brain"""
import requests
from nazca4sdk.datahandling.data_mod import Data


class BrainClient:
    """ Get data from Nazca4.0 Brain
    """

    def __init__(self):
        """Initialize Brain connection info"""
        # self.__brain_url = 'http://brain:8000'
        self.__brain_url = 'http://10.217.1.201:10334'
    def get_energy_quality(self, energy_input):
        """ Posting data to receive energy quality calculations from Brain"""
        return requests.post(f'{self.__brain_url}/energy/', json=energy_input)

    def get_vibration_quality(self, vibration_input):
        """ Posting data to receive vibration quality calculations from Brain"""
        return requests.post(f'{self.__brain_url}/vibration/', json=vibration_input)

    def get_oee_easy(self, oee_easy_input):
        """ Posting data to receive OEE value based on:
            Availability, Performance, Quality parameters from Brain """
        return requests.post(f'{self.__brain_url}/oee_easy/', json=oee_easy_input)

    def get_oee_full(self, oee_full_input):
        """ Posting data to receive oee value based on A, B, C, D, E, F parameters from Brain"""
        return requests.post(f'{self.__brain_url}/oee_full/', json=oee_full_input)

    def get_cp_pp_indicator(self, cp_pp_input):
        """
        Posting data to receive cp/pp indicator based on:
            lsl, usl, std parameters from Brain
        """
        
        return requests.post(f'{self.__brain_url}/cp_pp_indicator/', json=cp_pp_input)

    def get_cpk_ppk_indicator(self, cpk_ppk_input):
        """
        Posting data to receive cpk/ppk indicator based on:
            lsl, usl, mean, std parameters from Brain
        """
        return requests.post(f'{self.__brain_url}/cpk_ppk_indicator/', json=cpk_ppk_input)

    @staticmethod
    def parse_response(response):
        """ Parsing method"""
        if response.status_code == 200:
            json_response = response.json()
            if 'message' in json_response:
                print("Brain response failure")
                return None
            return Data(json_response)

        print("Brain response error")
        return None
