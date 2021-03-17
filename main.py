import os
from typing import Tuple, Union

import pandas as pd
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.tab import MDTabsLabel

from gui.behave import BaseDropBehaviour
from gui.uix import DataTableFull, DataTableMini, DataTableDescription, Tab, Tabs
from setting import BASE_DIR

from typing import List

ROW_INDEX_COLOR = (1,1,1,1)
ROW_HEIGHT = 50
ROW_INDEX_WIDTH = 40

class SystemToolbarLayout(AnchorLayout):
    anchor_x = "left"
    anchor_y = "center"

class SystemToolbar(BoxLayout):
    def a(self):
        print('Не трогай меня')

class SystemToolbarItem(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_x = None
        self.width = 30

class DataToolBarLayout(AnchorLayout):
    anchor_x = "right"
    anchor_y = "center"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class DataToolbar(BoxLayout):
    pass

class DataToolbarItem(AnchorLayout):
    anchor_x = "center"
    anchor_y = "center"
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = 50

class DataBox(MDBoxLayout):
    filepath: str = ''
    """ File path to the dropped image """

    data: pd.array = pd.array([])
    """ Represents the data of the file """

    orientation: str = "vertical"
    """ Orientate all childs vertically """

    def __init__(self, filepath: str, data: pd.array, **kwargs):
        self.filepath = filepath
        self.data = data
        self.filename = os.path.split(filepath)[-1]
        super().__init__(**kwargs)
        self.make_description()
    
    def make_data_table(self, *args:any):
        """ Makes a data table and adds it to the widget"""
        self.add_widget(
            DataTableMini(
                data=self.data,
        ))
    
    def make_description(self):
        """ Descriptive statistics include those that summarize
        the central tendency, dispersion and shape of a dataset’s distribution,
        excluding NaN values.
        """
        data = self.data.describe()
        self.add_widget(DataTableDescription(
            data=data,
        ))

class DropAnchorLayout(BoxLayout, BaseDropBehaviour):

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

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_delete_tab')

    def on_drop_file(self, filepath:str):
        """ Fills all needed properties and reads the file """
        if self.__same_data(filepath):
            return
        table_index = self.generate_new_table(filepath)
        self.dataTabs.dispatch('on_drop_file', filepath, table_index)
        self.pathInfo.dispatch('on_drop_file', filepath, table_index)

        self.show_table_by_index(table_index)

    def generate_new_table(self, filepath: str) -> str:
        """ Creates a new table, adds it to the data_tables and return its index """
        table = DataBox(
            filepath=filepath,
            data=pd.read_csv(filepath, sep=",", header=0)
        )
        # add the widget to manage it
        table_index = str(self.max_index)
        if not self.data_tables.get(table_index):
            self.data_tables[table_index] = table
            self.max_index += 1
        else:
            raise KeyError('there is same key in the data_table')
        return table_index

    def __same_data(self, filepath:str):
        for index, table in self.data_tables.items():
            if table.filepath == filepath:
                self.show_table_by_index(index)
                self.dataTabs.to_tab_by_index(index)
                return True
        return False

    def on_delete_tab(self, index: str):
        """ Calls when tab is deleted """
        try:
            table = self.data_tables[index] #!
            self.remove_widget(table)
            del self.data_tables[index]
        except KeyError:
            pass
    
    def show_table_by_index(self, index:str):
        """ Displays selected table and delete the current one """
        table = self.data_tables.get(index)
        
        if table:
            try:
                self.remove_widget(self.data_tables[self.curr_data_table]) # delete current
                self.prev_data_table = self.curr_data_table
            except KeyError:
                # no current tab
                pass
            self.curr_data_table = index
            self.add_widget(table)
    
class MyApp(MDApp):
    drops = []
    def build(self):
        Window.maximize()
        Window.clearcolor = (.2,.2,.2,1)
        Window.bind(on_dropfile=self.handledrops) # handle every drop
        self.root = Builder.load_file(os.path.join(BASE_DIR, 'gui', 'main.kv'))
    
    def handledrops(self, *args, **kwargs):
        """ Called every time when file is dropped in the app.
            Calls all drops functions witch added to drops
        """
        for f in self.drops:
            f(*args, **kwargs)
    
    def add_drop(self, f:callable):
        """ Adds a fanction to call when something if dropped to the screen"""
        self.drops.append(f)

MyApp = MyApp()
MyApp.run()
