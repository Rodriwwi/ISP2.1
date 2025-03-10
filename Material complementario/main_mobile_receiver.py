from transmitter_antenna import TransmitterAntenna
from rx_device import RxDevice
import math_utils as mu
import metrics


if __name__ == '__main__':

    # Input data (Problem 5)
    p_tx = 20  # mW
    p_noise = 5  # mW
    tx_gain = 10  # dBi
    freq_mhz = 140  # MHz
    bw = 20  # MHz
    rx_gain = 7  # dBi

    # Instance of TX element
    position_tx = (1, 1)
    tx_antenna = TransmitterAntenna("TX_1", position_tx, 20, bw, freq_mhz / 1000, mu.lineal_units_to_dbm(p_tx), tx_gain)

    # Instance of RX element
    array_positions_rx = [(300, 300), (200, 200), (100, 100)]

    first_position_rx = (-999, -999)  # The first position doest mind
    rx_antenna = RxDevice("RX_1", first_position_rx, 20, rx_gain, bw)

    for i in range(0, len(array_positions_rx)):
        current_position = array_positions_rx[i]

        # Change the position of the RX device
        rx_antenna.RX_position = current_position

        # Calculate distance
        distance = mu.calculate_distance(tx_antenna.TX_position, rx_antenna.RX_position)

        # Calculate free space path losses
        fspl = metrics.free_space_path_losses(distance, tx_antenna.TX_frequency)

        # Calculate received power from RX device
        rx_power_db = metrics.received_power(tx_antenna.TX_gain, rx_antenna.RX_gain, tx_antenna.TX_power, fspl)

        # Assignation of received power to RX object attribute
        rx_antenna.RX_power = rx_power_db

        # Print results
        print("Receiver power in position " + str(rx_antenna.RX_position) + ": " + str(rx_antenna.RX_power) + " dBm")
