import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display

class Calibration:
    def __init__(self, device):
        self.device = device
        self.calibration_pump_rotations_to_ml = {1: {1.0: 0.196, 2.0: 0.383, 10.0: 1.75, 20.0: 3.38, 45.0: 7.675, 95.0: 16.08},
 2: {2.0: 0.377, 20.0: 3.635, 42.0: 7.615, 50.0: 9.09, 72.0: 13.0},
 3: {},
 4: {1.0: 0.179,
  7.0: 1.218,
  20.0: 3.35,
  22.0: 3.685,
  50.0: 8.27,
  75.0: 12.425,
  86.0: 14.22}}

    def get_pump_coefficients_df(self):
        dev = self.device
        data = dev.calibration_coefs_pumps.copy()
        for p in dev.calibration_coefs_pumps:
            if data[p] == []:
                data.pop(p)
        pump_coefs_df = pd.DataFrame(data)
        pump_coefs_df.columns = ["pump %d"%p for p in pump_coefs_df.columns]
        pump_coefs_df.index = list("abcdefg"[:len(pump_coefs_df)])
        return pump_coefs_df

    def get_pump_rotations_to_ml_df(self):
        dev = self.device
        p1 = pd.DataFrame(dev.calibration_pump_rotations_to_ml[1], index=[1])
        p2 = pd.DataFrame(dev.calibration_pump_rotations_to_ml[2], index=[2])
        p3 = pd.DataFrame(dev.calibration_pump_rotations_to_ml[3], index=[3])
        p4 = pd.DataFrame(dev.calibration_pump_rotations_to_ml[4], index=[4])
        pump_rotations_to_ml_df = pd.concat([p1, p2, p3, p4])
        pump_rotations_to_ml_df = pump_rotations_to_ml_df / pump_rotations_to_ml_df.columns
        return pump_rotations_to_ml_df

    def get_od_coefficients_df(self):
        """
        Get the OD calibration coefficients for a device
        :param dev: device
        :return:
        """
        od_coefs_df = pd.DataFrame(self.device.calibration_coefs_od)
        od_coefs_df.columns = ["vial %d" % v for v in od_coefs_df.columns]
        od_coefs_df.index = list("abcde")
        return od_coefs_df

    def plot_pump_coefficients(self, ax=None):
        """
        Plot the pump calibration coefficients for a device
        :param dev: device
        :param ax:
        :return:
        """
        if ax is None:
            fig, ax = plt.subplots()
        pump_coefs_df = self.get_pump_coefficients_df()
        if any(pump_coefs_df.values.ravel()):
            pump_coefs_df.plot.bar(ax=ax)
        else:
            ax.set_title("No pump calibration coefficients")
        ax.set_title("Pump Calibration Coefficients")
        plt.show()

    def plot_pump_rotations_to_ml(self, ax=None):
        fig, ax = plt.subplots()
        pump_rotations_to_ml_df = self.get_pump_rotations_to_ml_df()
        for p in range(4):
            if len(pump_rotations_to_ml_df.iloc[p, :].dropna()):
                pump_rotations_to_ml_df.iloc[p, :].dropna().plot(ax=ax, style="o:", label="pump %d" % (p + 1))
        ax.legend()
        ax.set_ylabel("ml/rotation")
        ax.set_ylabel("total rotations")
        ax.set_title("Pump Calibration Data")
        plt.show()

    def plot_od_coefficients(self, ax=None):
        """
        Plot the OD calibration coefficients for a device
        :param dev: device
        :param ax:
        :return:
        """
        if ax is None:
            fig, ax = plt.subplots()
        od_coefs_df = self.get_od_coefficients_df()
        od_coefs_df.plot.bar(ax=ax)
        ax.set_title("OD Calibration Coefficients")
        plt.show()

    def plot_stirring_calibration(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()

        pd.DataFrame(self.device.calibration_fan_speed_to_duty_cycle).plot.bar(ax=ax)
        ax.set_title("Stirrer Calibration")
        ax.set_ylabel("Duty Cycle")
        ax.set_xlabel("Fan Speed")
        ax.set_xticklabels(["Low", "Medium", "High"])
        ax.set_xlabel("Stirring speed")
        plt.show()

    def display(self):
        self.plot_pump_coefficients()
        self.plot_pump_rotations_to_ml()
        self.plot_od_coefficients()
        self.plot_stirring_calibration()
        display(self.get_pump_coefficients_df())
        display(self.get_pump_rotations_to_ml_df())
        display(self.get_od_coefficients_df())
