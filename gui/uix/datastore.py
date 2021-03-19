import pandas as pd
from gui.behaviours.basedrop import BaseDropBehaviour
from gui.behaviours.switchtable import SwitchTableBehaviour
from gui.uix.datatablemini import DataTableMini
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from loguru import logger
from gui.uix.tabs import Tabs

class DataManager:
    data_tables: dict = {}
    """ Represent all data screens to fast switching """

    max_index: int = 0
    """ Represent current max index value in the data_tables keys  """

    def del_table(self, index:str):
        """ Remake data_table """
        try:
            del self.data_tables[index]
        except KeyError:
            logger(f"Try delete non existing table {index}")

    def get_table(self, index:str):
        """ Returns a table if it exists """
        return self.data_tables.get(index)

    def add_table(self, index:str, table:any):
        """ Adds a newly created table in the first position """
        self.data_tables[index] = table
        self.max_index += 1
    
    def get_all_tables(self):
        return self.data_tables.items()

class DataStore(
    BoxLayout,
    BaseDropBehaviour,
    SwitchTableBehaviour,
    DataManager,
    ):
    
    supported_ext: tuple = (
        "csv",
        )

    dataTabs: Tabs = ObjectProperty(None)
    """ Represent all data tabs """

    pathInfo = ObjectProperty(None)
    """ Path information instance """

    base_table = DataTableMini
    """ Base table to create when drop event occurs """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_drop_file(self, filepath: str):
        """ Reads the file, make DataTable and shows it """
        if self.same_data(filepath):
            return
        table_index = self.generate_new_table(filepath)
        self.dataTabs.dispatch('on_drop_file', filepath, table_index)
        self.pathInfo.dispatch('on_drop_file', filepath, table_index)

        self.dispatch("on_table_switch", table_index)

    def generate_new_table(self, filepath: str) -> str:
        """ Creates a new table, adds it to the data_tables and return its index """
        # add the widget to manage it
        table_index = str(self.max_index)
        if not self.get_table(table_index):
            table = self.base_table(
                filepath=filepath,
                data=pd.read_csv(filepath, sep=",", header=0)
            )
            self.add_table(table_index, table)
        else:
            raise KeyError(f'there is same key in the data_table {table_index}')
        return table_index

    def same_data(self, filepath:str) -> bool:
        for index, table in self.get_all_tables():
            if table.filepath == filepath:
                return True
        return False



