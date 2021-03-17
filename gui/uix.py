import os

import numpy as np
import pandas as pd
from kivy.event import EventDispatcher
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivymd.app import MDApp
from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.label import MDIcon, MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.tab import MDTabsBase

from .behave import TabSwitchBehavior
from .utils import PathStringShorter


class DataTableMini(MDDataTable):
    """ Mini data table with 5-6 first values and 5-6 end values """

    max_row: int = 12
    """ Max rows to display """

    def __init__(self, data: pd.array):
        mini_data = self.preform_data(data)
        super().__init__(
            size_hint=(1,1),
            column_data=[
                (x, dp(30)) for x in list(data)
            ],
            row_data=mini_data,
            rows_num=15
        )

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

    def on_row_press(self, *args):
        pass

class DataTableDescription(MDDataTable):
    """ Mini data table with 5-6 first values and 5-6 end values """

    max_row: int = 12
    """ Max rows to display """

    statistics: tuple = (
        'count', 'mean', 'std',
        'min', '25%', '50%', '75%',
        'max',
    )

    def __init__(self, data: pd.array):
        # here we have described data
        mod_data = self.preform_data(data)
        super().__init__(
            size_hint=(1,1),
            # empty columnt to add statistics
            column_data= [('Stat', dp(30))] + [(x, dp(30)) for x in list(data)],
            row_data=mod_data,
            rows_num=8
        )

    def preform_data(self, data: pd.array) -> np.array:
        """ Makes data suitable to the MDDataTable """
        """
        len(str(x).split('.')[-1]) - lendth of the floating part of a value
        """
        np_data = data.to_numpy()
        mod_data = []
        for idx, row in enumerate(np_data):
            mod_data.append([self.statistics[idx]] + [f"{x}" if len(str(x).split('.')[-1]) < 5 else f"{x:.5f}" for x in row])
        return mod_data

    def on_row_press(self, *args):
        pass

class DataTableFull(MDDataTable):
    """ Full table with all data, 25 rows by default per page """
    def __init__(self, data: pd.array):
        super().__init__(
            size_hint=(1,1),
            use_pagination=True,
            column_data=[
                (x, dp(30)) for x in list(data)
            ],
            row_data=[x for x in data.to_numpy()],
            rows_num=25,
            pagination_menu_pos='auto'
        )

    def if_shown_all_forward_dis(self):
        """ Currently its needed because in the original module there is no
            case when all data is shown
        """
        if self.rows_num > len(self.row_data):
            self.pagination.ids.button_forward.disabled = True
    
    def create_pagination_menu(self, interval):
        """ Redefine old pagination maker to restrict numbers of rows
            that can be displayed
        """
        menu_items = [
            {"text": f"{i}"}
            for i in range(
                self.rows_num, 101, self.rows_num,
            )
        ]
        pagination_menu = MDDropdownMenu(
            caller=self.pagination.ids.drop_item,
            items=menu_items,
            use_icon_item=False,
            position=self.pagination_menu_pos,
            max_height=self.pagination_menu_height,
            callback=self.table_data.set_number_displayed_lines,
            width_mult=2,
        )
        pagination_menu.bind(on_dismiss=self.table_data.close_pagination_menu)
        self.table_data.pagination_menu = pagination_menu

Builder.load_string(
"""
<Tab>:
    tab_label_inst: tab_label_inst
    size_hint_x: None
    orientation: "horizontal"
    ShortenLabel:
        id: tab_label_inst
        text: ''
        halign:'center'
        valign:'center'
        font_style: "Caption"
    MDIconButton:
        icon: "close"
        user_font_size: "13sp"
        on_release: root.on_ref_press()
"""
)


from kivy.clock import Clock


class ShortenLabel(MDLabel, PathStringShorter):

    max_filename_length: int = 20
    """ Same behaviour as max_directory_name_length """

    file_name_short_sign: str = "../."
    """ Sign that will be placed before extention of the file """

    parent_ = ObjectProperty(None)
    """ Instance of the Tab """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_text(self, filepath):
        self.text = self.shorten_file_name_by_filepath(filepath)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent_.on_tab_switch()
            if touch.is_double_tap:
                self.parent_.open_menu()
            return True

class Tab(BoxLayout):
    '''Class implementing content for a tab.'''

    tab_label_inst = ObjectProperty(None)
    """ Instance of the label """

    parent_ = ObjectProperty(None)
    """ Instance of the Tabs """

    state: str = "down"
    """ Current state of the tab """

    color: tuple = (0.55, 0.55, 0.55, 1)
    """ Default bg color """

    index: str = ""
    """ Index of the data table """

    filepath: str = ""
    """ Full path to the datafile """

    def __init__(self, parent_, index: str, filepath: str, **kwargs):
        super().__init__(**kwargs)
        self.width = 170
        self.parent_ = parent_
        self.index = index
        self.filepath = filepath
        self.tab_label_inst.parent_ = self
        self.tab_label_inst.update_text(filepath)
        self.create_menu()
        """ Index of the dataBox """

    def create_menu(self):
        menu_items = [
            {"text": f"{i}"}
            for i in range(
                10
            )
        ]
        self.tab_menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            use_icon_item=False,
            position="auto",
            max_height=300,
            # callback=self.table_data.set_number_displayed_lines,
            width_mult=2,
        )
        # tab_menu.bind(on_dismiss=self.table_data.close_pagination_menu)

    def open_menu(self):
        self.tab_menu.open()


    def set_state(self, state:str, color:tuple):
        self.state = state
        self.color = color
        self.do_background()

    def do_background(self):
        """ Draw a background """
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*self.color),
            Rectangle(
                size=self.size,
                pos=self.pos
            )
    
    def update(self):
        """ When position changes updates canvas """
        self.canvas.ask_update()
        self.do_background()
            
    def on_ref_press(self):
        """ Calls when close button is pressed """
        self.parent_.dispatch('on_ref_press', self)

    def on_tab_switch(self):
        """ Calls when close button is pressed """
        self.parent_.dispatch('on_tab_switch', self)


class Tabs(MDStackLayout, TabSwitchBehavior):
    """ It's not actual tab swithcer, just looks like this, only colors change """

    adaptive_width: bool = True

    current_active_tab = None

    prev_active_tab = None

    tab_active_color: tuple = (0.3, 0.3 ,0.3, 1)
    tab_normal_color: tuple = (0.55, 0.55, 0.55, 1)

    tab_states = {
        "down": tab_active_color,
        "up": tab_normal_color
    }

    dataStore = ObjectProperty(None)
    """ Where all dataBox'es are stored """

    pathInfo = ObjectProperty(None)
    """ Path information instance """

    def update_tabs(self, *args):
        """ Update drawing on all tabs """
        for tab in self.children:
            tab.update()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
            
    def on_drop_file(self, filepath, table_index):
        new_tab = Tab(
                    parent_=self,
                    index=table_index,
                    filepath=filepath, # be present as a filename
                )
        self.add_widget(new_tab)
        Clock.schedule_once(
            lambda x: self.set_current_active_tab(new_tab), 0.1
        )

    def set_current_active_tab(self, tab):
        try:
            self.current_active_tab.set_state('down', self.tab_states['down'])
        except AttributeError:
            pass
        try:
            tab.set_state('up', self.tab_states['up'])
        except AttributeError:
            # got NoneType
            pass

        self.prev_active_tab = self.current_active_tab
        self.current_active_tab = tab
    
    def set_non_active(self, tab):
        tab.set_state('down', self.tab_states['down'])

    def to_tab_by_index(self, index:str):
        """ Forse switch to tab """
        for tab in self.children:
            if tab.index == index:
                self.set_current_active_tab(tab)
                break
            
    def on_ref_press(
        self,
        tab_instance):
        self.remove_widget(tab_instance)
        self.dataStore.dispatch('on_delete_tab', tab_instance.index)
        self.pathInfo.dispatch('on_delete_tab', tab_instance.index)
        Clock.schedule_once(self.update_tabs, 0)
    
    def on_tab_switch(self, tab_instance):
        self.set_current_active_tab(tab_instance)
        self.dataStore.show_table_by_index(tab_instance.index)
        self.pathInfo.dispatch('on_tab_switch', tab_instance.filepath, tab_instance.index)

Builder.load_string(
"""
<PathInfo>:
    padding: 10,0,0,0
    path_label_inst: path_label_inst
    MDLabel:
        id: path_label_inst
        text: ""
        halign: "left"
        valign: "center"
        font_style: "Caption"
"""
)
class PathInfo(
    BoxLayout,
    TabSwitchBehavior,
    PathStringShorter
):
    """ BoxLayout represents a path to the opened file """

    path_label_inst = ObjectProperty(None)
    """ Label instance """

    labels: dict = {}
    """ If there are tabs their paths are stored here by index """

    max_directories_to_show: int = 5
    """ Maximum number of displayed directories
        filepath = "D:\Python_work\very_long_directory_name\show\me\your\love\love.py"
        Will be represented like so:
        filepath = "D: > Python_work > very_long_direc..\ > ... > love > love.py"
    """

    file_name_short_sign: str = '..'

    show_all_directories: bool = False
    """ If present ignore max_directories_to_show
        to display absolute path to the file
    """

    cur_index: str = '0'
    """ Curent displaied label index """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def on_delete_tab(self, index: str):
        try:
            del self.labels[index]
            if index == self.cur_index:
                self.path_label_inst.text = ""
        except KeyError:
            pass

    def on_tab_switch(self, filepath:str, index:str):
        """ Calls when tab is switching """
        self.place_breadcrumbs(filepath, index)
        self.cur_index = index

    def on_drop_file(self, filepath:str, index:str):
        """ Calls if you need to connect dropp event with tabs """
        self.place_breadcrumbs(filepath, index)
        self.cur_index = index
        
    def place_breadcrumbs(self, filepath:str, index:str):
        try:
            self.path_label_inst.text = self.labels[index]
            return
        except KeyError:
            pass
        nice_path = self.make_breadcrumbs(filepath)
        self.labels[index] = nice_path
        self.path_label_inst.text = nice_path

    def make_breadcrumbs(self, filepath: str) -> str:
        """ Makes spleted path representation
        """
        splited = os.path.split(filepath)
        dir_names = self.splited_filepath(splited[0])
        filename = splited[-1]
        del splited
        

        if len(dir_names) < self.max_directories_to_show or self.show_all_directories:
            nice_filepath = " > ".join(
                [self.shorten_directory_name(dir_name) for dir_name in dir_names] + \
                [self.shorten_file_name_by_filename(filename)]
            )
        else:
            part = self.max_directories_to_show // 2
            first_part = dir_names[:part]
            second_part = dir_names[-(self.max_directories_to_show-part):]
            nice_filepath = " > ".join(
                [self.shorten_directory_name(dir_name) for dir_name in first_part] + \
                ['...'] + \
                [self.shorten_directory_name(dir_name) for dir_name in second_part] + \
                [self.shorten_file_name_by_filename(filename)]
            )
        return nice_filepath
