from typing import *
import json


class RxDevice:
    """
        Attributes
        ----------
        - RX_id [str]: rx device identifier.
        - RX_position [tuple of floats]: current X and Y position of the rx devuce (related to the simulation scenario).
        - RX_height [float]: elevation of the rx device.
        - RX_gain [float]: receiver antenna gain.
        - RX_power [float]: power of the receiver device.
        - RX_bandwidth [float]: bandwidth allocated by the transmitter for the rx antenna link.

        Methods
        -------
        - __init__: Constructor. Parametrized the object according to the entered parameters.
        - __str__: information for output by file or by screen of results.
        - to_json: it dumps (in a json file) the values of the class attributes at each time instant.
    """

    RX_id: str = ""  # Example = "RX_1".
    RX_position: Tuple[float, float] = (0.0, 0.0)  # (x,y)
    RX_height: float = 0.0  # m
    RX_gain: float = 0.0  # dBi
    RX_power: float = 0.0  # dBm
    RX_bandwidth: float = 0.0  # MHz
    RX_steps: List = []
    connected_TX = ""

    def __init__(self, rx_id: str, first_position: Tuple[float, float], height: float, gain: float, assigned_bandwidth: float, steps_param: List):
        """
            'Init' method of the class 'RxDevice'.
            Constructor. Parametrized the object according to the entered parameters.

            :param rx_id: receiver device identifier -> Example: "RX_1".
            :param position: first X and Y position of the rx device (related to the simulation scenario -> (x,y).
            :param height: elevation of the rx device (in meters).
            :param gain: receiver antenna gain (in dBi).
            :param assigned_bandwidth: bandwidth allocated by the transmitter for the rx antenna link (in MHz).
        """

        self.RX_id = rx_id
        self.RX_position = first_position
        self.RX_height = height
        self.RX_gain = gain
        self.RX_bandwidth = assigned_bandwidth
        self.RX_power = -9999  # ¿?
        self.connected_TX = ""

        self.RX_steps = []
        self.RX_steps.append(self.RX_position)

        # Añadimos los pasos al vector de posiciones
        for i in range(0, len(steps_param)):
            self.RX_steps.append(steps_param[i])

    def __str__(self):
        """
            'To-string' method of the class 'RxDevice'.
            Information for output by file or by screen of results.
        """

        l1 = " - id: " + self.RX_id
        l2 = " - Current position: " + str(self.RX_position)
        l3 = " - Height: " + str(self.RX_height) + " m"
        l4 = " - Gain: " + str(self.RX_gain) + " dBi"
        l5 = " - RX power: " + str(self.RX_power) + "dBm"
        l6 = " - Assigned bandwidth: " + str(self.RX_bandwidth) + " MHz"

        return l1 + "\n" + l2 + "\n" + l3 + "\n" + l4 + "\n" + l5 + "\n" + l6

    def to_json(self, time: float, file_path: str):
        """
            It dumps (in a json file) the values of the class attributes at each time instant.

            :param time: time instant (in seconds).
            :param file_path: path to the folder containing the results files.
        """

        data_dump = dict()
        rx_device_data = dict()

        rx_device_data["id"] = self.RX_id
        rx_device_data["position"] = self.RX_position
        rx_device_data["height"] = self.RX_height
        rx_device_data["bandwidth"] = self.RX_bandwidth
        rx_device_data["gain"] = self.RX_gain
        rx_device_data["power"] = self.RX_power

        data_dump[time] = rx_device_data

        with open(file_path + self.RX_id, 'a') as json_file:
            json.dump(data_dump, json_file, indent=2, separators=(',', ': '))
