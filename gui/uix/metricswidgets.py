from kivy.uix.widget import Widget
from kivymd.app import MDApp



class MetricsWidgets:

    other_data_metrics: dict = {}
    """ Represent all conserning to data widget instances """

    shown_metrics_idxs: list = []
    """ Contains all shown metrics indexes """

    def place_new_tab(self, index:str, tab: Widget):
        """ Place a new wdiget over the table
            index: str - table index to which the new widget belongs
            tab: Widget - instance of the Widget class
        """
        if not self.other_data_metrics.get(index):
            self.other_data_metrics[index] = tab

        self.show_data_metrics(index)
        
    def show_data_metrics(self, index:str):
        metric = self.other_data_metrics.get(index)
        app = MDApp.get_running_app()
        if metric:
            self.shown_metrics_idxs.append(index)
            self.add_widget(metric) #!!!