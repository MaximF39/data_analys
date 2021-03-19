from kivy.uix.widget import Widget
from kivymd.app import MDApp
from loguru import logger
from gui.uix.datatabledescr import DataTableDescription
from kivy.properties import ObjectProperty
from gui.uix.tabs import Tabs


class MetricsWidgets:
    """  """

    data_tables: dict = {}
    """ Represent all conserning to data widget instances """

    shown_metrics_idxs: list = []
    """ Contains all shown metrics indexes """

    curr_data_table:str = '0'
    """ Index if the current data_table """

    dataTabs: Tabs = ObjectProperty(None)
    """ Represent all data tabs """
    
    def get_metric_index(self, index:str, metric_name:str) -> str:
        """ Makes a metric index """
        return f"{index}_{metric_name}"

    def is_not_metric(self, index:str):
        """ If an underline is in an index it's a metric """
        if len(index.split('_')) > 1:
            return False # It's metric
        return True # Not metric

    def __place_new_tab(self, index:str, widget: Widget, metric_name:str):
        """ Place a new widget with a new tab
            index: str - table index to which the new widget belongs
            tab: Widget - instance of the Widget class
        """
        m_index = self.get_metric_index(index, metric_name)

        if not self.data_tables.get(m_index):
            self.data_tables[m_index] = widget
        self.__show_data_metrics(m_index)
        
    def __show_data_metrics(self, m_index:str):
        """ Very similar with on_drop_file """
        metric = self.data_tables.get(m_index)
        if metric:
            self.shown_metrics_idxs.append(m_index)
            self.dataTabs.dispatch('on_drop_file', metric.filepath, m_index)
            self.dispatch("on_table_switch", m_index)

    def remake_non_numeric_data(self):
        try:
            table = self.data_tables.get(self.curr_data_table)
        except KeyError:
            logger.warning("Calls when there's no opened data table")

    def create_description(self):
        """ If there's opened data table makes a description for it 
            and place it on a new tab
        """
        metric_name = "description"
        
        if self.__metric_can_be_made(metric_name):
            tb = self.data_tables[self.curr_data_table]
            metric = DataTableDescription(
                tb.filepath,
                tb.data
            )
            del tb
            self.__place_new_tab(self.curr_data_table, metric, metric_name)
    
    def __metric_can_be_made(self, metric_name:str) -> bool:
        """ Checks if metric can be created.
            Metric can be created if:
                there's no such metric in data_tables
            It garanties that self.curr_data_table index refers to a proper widget
        """
        index = self.curr_data_table
        metric_index = self.get_metric_index(index, metric_name)
        active_table = self.data_tables.get(index) # table
        active_metric = self.data_tables.get(metric_index)
        if active_metric:
            self.dispatch('on_table_switch', metric_index)
            self.dataTabs.to_tab_by_index(metric_index)
            return False
        if active_table and self.is_not_metric(index):
            return True
        return False

