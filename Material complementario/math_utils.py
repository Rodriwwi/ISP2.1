from typing import *
import math as m


def lineal_units_to_dbm(num: float):
    """
        Transform linear data to logarithmic scale

        :param num: value to transform (in linear units).
        :return x: value transformed to logarithmic scale (in dB).
    """

    x = 10*m.log10(num)

    return x


def dbm_to_lineal_units(num_dbm: float):
    """
        Transform logarithmic data to lineal scale

        :param num_dbm: value to transform (in dB).
        :return x: value transformed to lineal scale (in linear units).
    """

    x = 10**(num_dbm/10)

    return x


def calculate_distance(tx_pos: Tuple[float, float], rx_pos: Tuple[float, float]):
    """
        Calculation of the euclidean distance between two points.

        :param tx_pos: x and y position of the transmitter antenna.
        :param rx_pos: x and y position of the receiver antenna.
        :return dist: distance between two points (in meters).
    """

    # Euclidean distance formula (vector module)
    dist = m.sqrt((rx_pos[0]-tx_pos[0])**2 + (rx_pos[1]-tx_pos[1])**2)

    return dist
