import os

from kivy.core.window import Window
from kivy.event import EventDispatcher
from kivymd.app import MDApp


class BaseDropBehaviour(EventDispatcher):
    """ Base drop behaviour when something is dropped
        in the widget area
    """
    supported_ext: tuple = ()
    """ Represents all supported extentions """

    support_all_files: bool = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_drop_file')
        # get app instance to add function from widget
        app = MDApp.get_running_app()
        # add function to the list
        app.add_drop(self._on_drop)

    def _on_drop(self, window, file_path:str):
        """ Id the user dropped something to the widget area """
        # checks drop position
        if self.collide_point(*Window.mouse_pos):
            filepath_path = file_path.decode('utf-8')
            if self._supported(filepath_path):
                self.dispatch('on_drop_file', filepath_path)
            else:
                # make a pop up message
                print('File is not supported')
    
    def process_file(self, file_path:str):
        """ Fills all needed properties and reads the file """
        raise NotImplementedError(f"Method does not implemented 'process_file'")

    def _supported(self, file_path:str):
        """ Checks if the dropped file is supported to process """
        if self.support_all_files:
            return True
        filename = os.path.split(file_path)[-1]
        if filename.split('.')[-1] in self.supported_ext:
            return True
        return False
