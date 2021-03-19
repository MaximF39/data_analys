from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDIconButton
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
"""
)
from kivy.uix.behaviors import ButtonBehavior


class DataToolbar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)



class DataToolbarItem(MDIconButton):
    pass
