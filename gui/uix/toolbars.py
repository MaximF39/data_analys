from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDTextButton
from gui.uix.datatabledescr import DataTableDescription
from gui.uix.datastore import DataStore

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

    dataStore: DataStore = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_description(self):
        """ Create and opens a new tab with described data """
        self.dataStore.create_description()

    def remake_non_numeric_data(self):
        """ Opens a new screen to redact data by hands """
        self.dataStore.remake_non_numeric_data()

class DataToolbarItem(MDTextButton):
    pass
