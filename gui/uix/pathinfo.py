import os

from gui.behaviours.switchtab import TabSwitchBehavior
from gui.utils.pathshorter import PathStringShorter
from kivy.lang import Builder
from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

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
    PathStringShorter):
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
