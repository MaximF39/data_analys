import pandas as pd
from gui.uix.basedatatable import BaseDataTable
from kivymd.uix.datatables import CellRow, CellHeader
from functools import partial

class DataTableMini(BaseDataTable):
    """ Mini data table with 5-6 first values and 5-6 end values """

    max_row: int = 12
    """ Max rows to display """

    def __init__(self, filepath:str, data: pd.array):
        super().__init__(filepath, data)

    def preform_data(self, data: pd.array) -> list:
        """ Makes data suitable to the MDDataTable """
        np_data = data.to_numpy()
        if self.max_row > data.shape[0]:
            # not enough rows in data
            return [x for x in np_data]
        part = self.max_row // 2
        head = [x for x in np_data[:part]]
        middle = [['...' for _ in range(data.shape[1])]]
        tail = [x for x in np_data[-part:]]
        return head + middle + tail