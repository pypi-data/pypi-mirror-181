__version__ = "0.0.60"

# from .device.base_device import BaseDevice
# from .device.morbidostat_device import MorbidostatDevice
# from .culture import TurbidostatCulture, MorbidostatCulture
from .experiment import Experiment
from .GUI.notifier import Notifier
from . import util
from IPython.display import display
import subprocess
import sys
_main_gui = None


def upgrade_replifactory():
    print("upgrading replifactory...")
    output = subprocess.check_output([sys.executable, "-m", "pip", "install", "--upgrade", "replifactory"])
    print(output.decode("utf-8"))


def gui():
    from .GUI.main_gui import MainGuiBuilder
    global _main_gui
    if _main_gui is None:
        _main_gui = MainGuiBuilder()

    display(_main_gui.widget)
