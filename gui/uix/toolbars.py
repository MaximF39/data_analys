from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDTextButton
from gui.uix.datatabledescr import DataTableDescription

Builder.load_string(
"""
<DataToolbar>:
    orientation: "vertical"
    size_hint: None, None
    width: IMAGE_TOOLBAR_WIDTH
    height: 500
    canvas.before:
        Color:
            rgb: .3,.3,.3
        Rectangle:
            size: self.size
            pos: self.pos

<DataToolbarItem>:
    text: 'File'
"""
)
from kivy.uix.behaviors import ButtonBehavior


class DataToolbar(BoxLayout):

    dataStore = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_description(self):
        index = self.dataStore.curr_data_table
        active_table = self.dataStore.data_tables.get(index)
        if active_table:
            metric = DataTableDescription(
                active_table.filepath,
                active_table.data
            )
            self.dataStore.place_new_tab(index, metric)

class DataToolbarItem(MDTextButton):
    pass
