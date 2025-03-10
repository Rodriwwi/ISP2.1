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
    position_tx = (5, 5)
    tx_antenna = TransmitterAntenna("TX_1", position_tx, 20, bw, freq_mhz / 1000, mu.lineal_units_to_dbm(p_tx), tx_gain)

    # Instance of RX element
    position_rx = (1, 1)
    rx_antenna = RxDevice("RX_1", position_rx, 20, rx_gain, bw)

    # Calculate distance
    distance = mu.calculate_distance(tx_antenna.TX_position, rx_antenna.RX_position)

    # Calculate free space path losses
    fspl = metrics.free_space_path_losses(distance, tx_antenna.TX_frequency)

    # Calculate received power from RX device
    rx_power_db = metrics.received_power(tx_antenna.TX_gain, rx_antenna.RX_gain, tx_antenna.TX_power, fspl)

    # Assignation of received power to RX object attribute
    rx_antenna.RX_power = rx_power_db

    # Calculate SNR (using SINR module with zero interference)
    snr = metrics.calculate_sinr(rx_antenna.RX_power, p_noise, 0)

    # Calculate capacity
    capacity = metrics.capacity(tx_antenna.TX_bandwidth, mu.dbm_to_lineal_units(snr))

    # Print results
    print("Link capacity: " + str(capacity) + " Mbps")
