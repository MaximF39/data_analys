import pandas as pd
from gui.behaviours.basedrop import BaseDropBehaviour
from gui.behaviours.switchtable import SwitchTableBehaviour
from gui.uix.datatablemini import DataTableMini
from gui.uix.metricswidgets import MetricsWidgets
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class DataStore(
    BoxLayout,
    BaseDropBehaviour,
    SwitchTableBehaviour,
    MetricsWidgets,
):
    supported_ext: tuple = (
        "csv",
    )
    support_all_files: bool = False

    data_tables: dict = {}
    """ Represent all data screens to fast switching """

    max_index: int = 0
    """ Represent current max index value in the data_tables keys  """

    dataTabs = ObjectProperty(None)
    """ Represent all data tabs """

    pathInfo = ObjectProperty(None)
    """ Path information instance """

    prev_data_table: str = '0'
    """ Index if the previous data_table """

    curr_data_table: str = '0'
    """ Index if the current data_table """

    base_table = DataTableMini
    """ Base table to create when drop event occurs """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_delete_tab')

    def on_drop_file(self, filepath: str):
        """ Reads the file, make DataTable and shows it """
        if self.__same_data(filepath):
            return
        table_index = self.generate_new_table(filepath)
        self.dataTabs.dispatch('on_drop_file', filepath, table_index)
        self.pathInfo.dispatch('on_drop_file', filepath, table_index)

        self.dispatch("on_table_switch", table_index)

    def generate_new_table(self, filepath: str) -> str:
        """ Creates a new table, adds it to the data_tables and return its index """
        # add the widget to manage it
        table_index = str(self.max_index)
        if not self.data_tables.get(table_index):
            table = self.base_table(
                filepath=filepath,
                data=pd.read_csv(filepath, sep=",", header=0)
            )
            self.data_tables[table_index] = table
            self.max_index += 1
        else:
            raise KeyError('there is same key in the data_table')
        return table_index

    def __same_data(self, filepath: str):
        """ Checks if Datable is already on the screen, if so, shows it """
        for index, table in self.data_tables.items():
            if table.filepath == filepath:
                self.dispatch("on_table_switch", index)
                self.dataTabs.to_tab_by_index(index)
                return True
        return False

    def on_delete_tab(self, index: str):
        """ Calls when tab is deleted """
        try:
            table = self.data_tables[index]  # !
            self.remove_widget(table)
            del self.data_tables[index]
        except KeyError:
            pass
'''
    def on_edit_table(self, index: str, filepath: str) -> str:
        table_index = str(self.max_index)
        if not self.data_tables.get(table_index):
            table = self.base_table(
                filepath=filepath,
                data=pd.read_csv(filepath, sep=",", header=0)
            )
            self.data_tables[table_index] = table
            self.max_index += 1
        else:
            raise KeyError('there is same key in the data_table')
        return table_index
'''