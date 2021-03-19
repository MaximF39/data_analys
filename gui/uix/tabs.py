
from gui.behaviours.switchtab import TabSwitchBehavior
from gui.utils.pathshorter import PathStringShorter
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.stacklayout import MDStackLayout

Builder.load_string(
"""
<Tab>:
    tab_label_inst: tab_label_inst
    size_hint_x: None
    orientation: "horizontal"
    ShortenLabel:
        id: tab_label_inst
        halign:'center'
        valign:'center'
        font_style: "Body2"
        theme_text_color: "Custom"
        text_color: .9,.9,.9,1
    MDIconButton:
        icon: "close"
        ripple_rad_default: 0.5
        user_font_size: "15sp"
        on_release: root.close_pressed()
"""
)
class ShortenLabel(MDLabel, PathStringShorter):

    max_filename_length: int = 20
    """ Same behaviour as max_directory_name_length """

    file_name_short_sign: str = "../."
    """ Sign that will be placed before extention of the file """

    parent_ = ObjectProperty(None)
    """ Instance of the Tab """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def update_text(self, filepath: str):
        self.text = self.shorten_file_name_by_filepath(filepath)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.parent_.on_tab_switch()
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
        """ Index of the dataBox """
        self.filepath = filepath
        self.tab_label_inst.parent_ = self
        self.tab_label_inst.update_text(filepath)

    def set_state(self, state:str, color:tuple):
        """ Sets current state to tab and change its color """
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
            
    def close_pressed(self):
        """ Calls when close button is pressed """
        self.parent_.dispatch('on_delete_tab', self)

    def on_tab_switch(self):
        """ Calls when close button is pressed """
        self.parent_.dispatch('on_tab_switch', self)

class Tabs(MDStackLayout, TabSwitchBehavior):
    """ It's not actual tab swithcer, just looks like this, only colors change """

    adaptive_width: bool = True

    curr_tab_idx = None

    prev_tab_idx = None

    tab_active_color: tuple = (0.55, 0.55 ,0.55, 1)
    tab_normal_color: tuple = (0.3, 0.3, 0.3, 1)

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
            
    def on_drop_file(self, filepath:str, table_index:str):
        new_tab = Tab(
                    parent_=self,
                    index=table_index,
                    filepath=filepath, # be present as a filename
                )
        self.add_widget(new_tab)
        Clock.schedule_once(
            lambda x: self.set_current_active_tab(new_tab), 0
        )

    def set_current_active_tab(self, tab):
        try:
            self.curr_tab_idx.set_state('up', self.tab_states['up'])
        except AttributeError:
            # curr_tab_idx is None
            pass
        tab.set_state('down', self.tab_states['down'])
        self.prev_tab_idx = self.curr_tab_idx
        self.curr_tab_idx= tab
    
    def to_tab_by_index(self, index:str):
        """ Forse switch to tab """
        for tab in self.children:
            if tab.index == index:
                self.set_current_active_tab(tab)
                break
            
    def on_delete_tab(self, tab_instance:Tab):
        self.remove_widget(tab_instance)
        self.dataStore.dispatch('on_delete_tab', tab_instance.index)
        self.pathInfo.dispatch('on_delete_tab', tab_instance.index)
        Clock.schedule_once(self.update_tabs, 0)
    
    def on_tab_switch(self, tab_instance):
        self.set_current_active_tab(tab_instance)
        self.dataStore.dispatch("on_tab_switch", tab_instance.index)
        self.pathInfo.dispatch('on_tab_switch', tab_instance.filepath, tab_instance.index)
