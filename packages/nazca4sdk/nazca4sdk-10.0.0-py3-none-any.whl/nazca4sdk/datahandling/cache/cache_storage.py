from nazca4sdk.datahandling.cache.key_value import KeyValue
from nazca4sdk.datahandling.open_data_client import OpenDataClient


class CacheStorage:
    """Allow user to read and write value to Cache

    """

    def __init__(self, https=True):
        self.__openData = OpenDataClient(https)

    def read_keys(self, keys):
        """Read cache values for list of keys
        
        Args:
            keys - list of keys to read
        Returns:
            List of cache entry
        """
        return self.__openData.read_cache_keys(keys)

    def write_keys(self, key_values: KeyValue):
        """
        Write key value to cache

        Args:
            key_values:  key value to write in cache

        Returns:
             CacheEntry if success or None if error
        """
        return self.__openData.write_cache_keys(key_values)
