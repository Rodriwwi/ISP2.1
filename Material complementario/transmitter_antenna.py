from typing import *
import json


class TransmitterAntenna:
    """
        Attributes
        ----------
        - TX_id [str]: transmitter identifier.
        - TX_position [tuple of floats]: current X and Y position of the transmitter (related to the simulation scenario).
        - TX_height [float]: height of the antenna transmitter.
        - TX_bandwidth [float]: bandwidth allocated by the transmitter for the communication link.
        - TX_frequency [float]: operational frequency.
        - TX_power [float]: transmitter power.
        - TX_gain [float]: gain of the transmitter antenna.

        Methods
        -------
        - __init__: Constructor. Parametrized the object according to the entered parameters.
        - __str__: information for output by file or by screen of results.
        - to_dict: it creates a dictionary with the values of the object to be used by the subclass to dump the values into a json file.
    """

    TX_id: str = ""  # Example = "TX_1"
    TX_position: Tuple[float, float] = (0.0, 0.0)  # (x,y)
    TX_height: float = 0.0  # m
    TX_bandwidth: float = 0.0  # MHz
    TX_frequency: float = 0.0  # GHz
    TX_power: float = 0.0  # dBm
    TX_gain: float = 0.0  # dBi

    def __init__(self, tx_id: str, position: Tuple[float, float], height: float, bandwidth: float, frequency: float, p_tx: float, gain: float):
        """
            'Init' method of the class 'TransmitterAntenna'.
            Constructor. Parametrized the object according to the entered parameters.

            :param tx_id: transmitter antenna identifier -> Example = "TX_1".
            :param position: current X and Y position of the transmitter antenna -> (x,y).
            :param height: elevation of the transmitter antenna (in meters).
            :param bandwidth: bandwidth allocated by the transmitter for the communication link (in MHz).
            :param frequency: operational frequency (in GHz)
            :param p_tx: transmitter power (in dBm).
            :param gain: gain of the antenna (in dBi).

            :raise ConfigurationNotFound: occurs when the configuration entered by parameters is not implemented in the simulator.
        """

        self.TX_id = tx_id
        self.TX_position = position
        self.TX_height = height
        self.TX_bandwidth = bandwidth 
        self.TX_frequency = frequency
        self.TX_gain = gain
        self.TX_power = p_tx

    def __str__(self):
        """
            'To-string' method of the class 'TransmitterAntenna'.
            Information for output by file or by screen of results.
        """

        l1 = " - id: " + self.TX_id
        l2 = " - Current position: " + str(self.TX_position)
        l3 = " - TX Gain: " + str(self.TX_gain) + " dBi"
        l4 = " - TX power: " + str(self.TX_power) + " dBm"
        l5 = " - Height: " + str(self.TX_height) + " m"
        l6 = " - Operational frequency: " + str(self.TX_frequency) + " GHz"
        l7 = " - Available bandwidth: " + str(self.TX_bandwidth) + " MHz"

        return l1 + "\n" + l2 + "\n" + l3 + "\n" + l4 + "\n" + l5 + "\n" + l6 + "\n" + l7

    def to_json(self, time: float, file_path: str):
        """
            It dumps (in a json file) the values of the class attributes at each time instant.

            :param time: time instant (in seconds)
            :param file_path: path to the folder containing the results files.
        """

        data_dump = dict()
        tx_antenna_data = dict()

        tx_antenna_data["id"] = self.TX_id
        tx_antenna_data["position"] = self.TX_position
        tx_antenna_data["height"] = self.TX_height
        tx_antenna_data["bandwidth"] = self.TX_bandwidth
        tx_antenna_data["frequency"] = self.TX_frequency
        tx_antenna_data["gain"] = self.TX_gain
        tx_antenna_data["power"] = self.TX_power

        data_dump[time] = tx_antenna_data

        with open(file_path + self.TX_id, 'a') as json_file:
            json.dump(data_dump, json_file, indent=2, separators=(',', ': '))
