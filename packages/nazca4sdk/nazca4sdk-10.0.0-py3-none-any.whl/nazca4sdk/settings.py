""" Nazca4SDK settings"""
import os

CONFIG_FILE_LOCATION_KEY = "CONFIG_FILE_LOCATION"
os.environ[CONFIG_FILE_LOCATION_KEY] = "Configure.yaml"


def set_config_file(file):
    """Set location of config file"""
    os.environ[CONFIG_FILE_LOCATION_KEY] = file
