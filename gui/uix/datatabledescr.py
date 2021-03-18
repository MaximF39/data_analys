import pandas as pd
from kivy.metrics import dp
from gui.uix.basedatatable import BaseDataTable


class DataTableDescription(BaseDataTable):
    """ Data table with description of the data includes 8 statistics """

    max_row: int = 12
    """ Max rows to display """

    statistics: tuple = (
        'count', 'mean', 'std',
        'min', '25%', '50%', '75%',
        'max',
    )
    rows_num: int = 8

    def __init__(self, filepath:str, data:pd.array):
        data = data.describe()
        super().__init__(filepath, data)

    def preform_data(self, data: pd.array) ->   list:
        """ Makes data suitable to the MDDataTable """
        """
        len(str(x).split('.')[-1]) - lendth of the floating part of a value
        """
        np_data = data.to_numpy()
        mod_data = []
        for idx, row in enumerate(np_data):
            mod_data.append([self.statistics[idx]] + [f"{x}" if len(str(x).split('.')[-1]) < 5 else f"{x:.5f}" for x in row])
        return mod_data

    def preform_column(slef, data:pd.array):
        """ Adds one column at the beginning """
        return [('Stat', dp(30))] + [(x, dp(30)) for x in list(data)]