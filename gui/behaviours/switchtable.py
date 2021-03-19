from gui.behaviours.switchtab import TabSwitchBehavior
from loguru import logger


class SwitchTableBehaviour(TabSwitchBehavior):
    """ Allows swtich tables by tabs """

    data_tables: dict = {}
    """ Represent all data screens to fast switching """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_table_switch')

    def on_tab_switch(self, index:str):
        self.dispatch("on_table_switch", index)

    def on_table_switch(self, index:str):
        """ Displays selected table and delete the current one """
        table = self.data_tables.get(index)
        if table:
            try:
                self.remove_widget(self.data_tables[self.curr_data_table]) # delete current
            except KeyError:
                logger.warning(f"Try to remove table with index {index} when there's no such table in the screen")
            self.curr_data_table = index
            self.add_widget(table)