""" Data_mod module"""
import pandas as pd


class Data:
    """
    Modification structure of data received from OpenData
    """
    def __init__(self, variable):
        self.__data = variable

    def to_df(self):
        """
        Returns DataFrame from received input

        Example:
            df = Data(selected_data).to_df()
        """
        if self.__is_empty():
            return []

        data_df = pd.json_normalize(self.__data)

        try:
            if 'measureTime' in data_df.columns:
                return data_df.sort_values(by='measureTime', ascending=True, ignore_index=True)
        except NameError:
            print('Error, measureTime column missing in dataframe')

    def data_to_list(self):
        """
        Method to modify data structure to list
        """

        return self.__data.values.tolist()

    def data_to_numpy(self):
        """
        Method to modify data structure to numpy array
        """

        return self.__data.to_numpy()

    def __is_empty(self):
        return len(self.__data) == 0
