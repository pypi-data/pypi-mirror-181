import ipywidgets as widgets
from IPython.core.display import clear_output
from IPython.display import display
from ipywidgets import VBox, Layout


class StatusTab:
    title = "Status"

    def __init__(self, main_gui):
        self.main_gui = main_gui
        self.refresh_button = widgets.Button(icon="fa-sync-alt", tooltip="Refresh", button_style="info",
                                             layout=Layout(width="35px"))
        self.output = widgets.Output()
        self.refresh_button.on_click(self.handle_button_action)
        self.widget = VBox([self.refresh_button, self.output])

    def handle_button_action(self, button):
        with self.output:
            clear_output()
            # self.main_gui.experiment.status.print_exp_status(increase_verbosity=True)
            dfconfig, dfrun = self.main_gui.experiment.status.status_df()
            print("CONFIGURATION PARAMETERS:")
            display(dfconfig)
            print("OPERATION PARAMETERS:")
            display(dfrun)

