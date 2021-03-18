from kivy.event import EventDispatcher


class TabSwitchBehavior(EventDispatcher):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.register_event_type('on_ref_press')
        self.register_event_type('on_drop_file')
        self.register_event_type('on_tab_switch')
        self.register_event_type('on_delete_tab')

    def on_ref_press(self, *args, **kwargs):
        """ Calls when close button in a tab is pressed """

    def on_tab_switch(self, *args, **kwargs):
        """ Calls when tab is switching """

    def on_delete_tab(self, *args, **kwargs):
        """ Calls when tab is deleteting """

    def on_drop_file(self, *args, **kwargs):
        """ Calls if you need to connect dropp event with tabs """