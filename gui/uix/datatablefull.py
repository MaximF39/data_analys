import pandas as pd
from gui.uix.basedatatable import BaseDataTable

class DataTableFull(BaseDataTable):
    """ Full table with all data, 25 rows by default per page """

    rows_num: int = 25

    use_pagination: bool = True,

    def __init__(self, filepath:str, data: pd.array):
        super().__init__(filepath, data)

    def if_shown_all_forward_dis(self):
        """ Currently its needed because in the original module there is no
            case when all data is shown
        """
        if self.rows_num > len(self.row_data):
            self.pagination.ids.button_forward.disabled = True
    
    def create_pagination_menu(self, interval):
        """ Redefine old pagination maker to restrict numbers of rows
            that can be displayed
        """
        menu_items = [
            {"text": f"{i}"}
            for i in range(
                self.rows_num, 101, self.rows_num,
            )
        ]
        pagination_menu = MDDropdownMenu(
            caller=self.pagination.ids.drop_item,
            items=menu_items,
            use_icon_item=False,
            position=self.pagination_menu_pos,
            max_height=self.pagination_menu_height,
            callback=self.table_data.set_number_displayed_lines,
            width_mult=2,
        )
        pagination_menu.bind(on_dismiss=self.table_data.close_pagination_menu)
        self.table_data.pagination_menu = pagination_menu