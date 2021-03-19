from gui.behaviours.switchtab import TabSwitchBehavior
from loguru import logger


class SwitchTableBehaviour(TabSwitchBehavior):
    """ Allows swtich tables by tabs, must be parent of DataStore """

    prev_table_idx: str = '0'
    """ Index if the previous data_table """

    curr_table_idx: str = '0'
    """ Index if the current data_table """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_table_switch')

    def on_tab_switch(self, index:str):
        self.dispatch("on_table_switch", index)

    @property
    def get_cur_table_index(self):
        return self.curr_table_idx

    def on_table_switch(self, index:str):
        """ Displays selected table and delete the current one """
        table = self.get_table(index)
        if table:
            current_table = self.get_table(self.curr_table_idx)
            try:
                self.remove_widget(current_table)
            except AttributeError:
                logger.warning(f"Try to replace table {self.curr_table_idx} when it's not shown")
            self.curr_table_idx = index
            self.add_widget(table)
    
    def on_delete_tab(self, index: str):
        """ Calls when tab is deleted """
        try:
            self.remove_widget(self.get_table(index))
            self.del_table(index)
        except AttributeError:
            logger.warning(f"Try to delete table when there's no such table {index}")