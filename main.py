import os

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp

from gui.uix.tabs import Tabs
from gui.uix.datastore import DataStore
from gui.uix.toolbars import DataToolbar
from gui.uix.pathinfo import PathInfo
from gui.uix.metricswidgets import Metrics
from setting import BASE_DIR


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
