import os

import pandas as pd
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable


class BaseDataTable(MDDataTable):
    filepath: str = ''
    """ File path to the dropped image """

    filename: str = ""
    """ A filename with an extention """

    data: pd.array = pd.array([])
    """ Represents the data of the file """

    rows_num: int = 15
    """ Default number of rows to display if possible """

    base_dp: int = 30
    """ Convert from density-independent pixels to pixels """

    use_pagination: bool = False
    """ If present pagination will be added """

    pagination_menu_pos:str = 'auto'
    """ Pagination will be placed by auto calculation """

    elevation: int = 0
    """ No shadows """

    def on_touch_down(self, touch):
        """ ModalView overlays all widgets, so
            the func propagates the touch to under layers
            Do not play smth under the table, it will be pressed
        """
        res = super().on_touch_down(touch)
        return False

    def __init__(self, filepath: str, data: pd.array):
        self.filepath = filepath
        self.data = data
        self.filename = os.path.split(filepath)[-1]
        super().__init__(
            column_data=self.preform_column(data),
            row_data=self.preform_data(data),
        )

    def preform_data(self, data:pd.array) -> list:
        """ Base method to preform data to show """
        return [x for x in data.to_numpy()]
    
    def preform_column(self, data:pd.array) -> list:
        """ Base method to preform column titles """
        return [(x, dp(self.base_dp)) for x in list(data)]
