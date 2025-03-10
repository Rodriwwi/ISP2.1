from transmitter_antenna import TransmitterAntenna
from rx_device import RxDevice
import math_utils as mu
import metrics


if __name__ == '__main__':

    # Input data (Problem 3)
    p_noise = 5  # mW
    freq_mhz = 700  # MHz
    bw = 25  # MHz
    rx_gain = 7  # dBi
    p_tx_1 = 14  # mW
    tx_gain_1 = 9  # dBi
    p_tx_2 = 8  # mW
    tx_gain_2 = 8  # dBi
    p_tx_3 = 10  # mW
    tx_gain_3 = 11  # dBi

    # Instance of TX element
    position_tx_1 = (25, 2)
    tx_antenna_1 = TransmitterAntenna("TX_1", position_tx_1, 20, bw, freq_mhz / 1000, mu.lineal_units_to_dbm(p_tx_1), tx_gain_1)

    position_tx_2 = (35, 30)
    tx_antenna_2 = TransmitterAntenna("TX_2", position_tx_2, 20, bw, freq_mhz / 1000, mu.lineal_units_to_dbm(p_tx_2), tx_gain_2)

    position_tx_3 = (10, 30)
    tx_antenna_3 = TransmitterAntenna("TX_3", position_tx_3, 20, bw, freq_mhz / 1000, mu.lineal_units_to_dbm(p_tx_3), tx_gain_3)

    # Save objects in dict structure
    tx_antennas = dict()
    tx_antennas[tx_antenna_1.TX_id] = tx_antenna_1
    tx_antennas[tx_antenna_2.TX_id] = tx_antenna_2
    tx_antennas[tx_antenna_3.TX_id] = tx_antenna_3

    # Instance of RX element
    position_rx = (25, 25)
    rx_antenna = RxDevice("RX_1", position_rx, 20, rx_gain, bw)

    # Calculate free space path losses
    losses = dict()
    losses[tx_antenna_1.TX_id] = metrics.free_space_path_losses(mu.calculate_distance(tx_antenna_1.TX_position, rx_antenna.RX_position), tx_antenna_1.TX_frequency)
    losses[tx_antenna_2.TX_id] = metrics.free_space_path_losses(mu.calculate_distance(tx_antenna_2.TX_position, rx_antenna.RX_position), tx_antenna_2.TX_frequency)
    losses[tx_antenna_3.TX_id] = metrics.free_space_path_losses(mu.calculate_distance(tx_antenna_3.TX_position, rx_antenna.RX_position), tx_antenna_3.TX_frequency)

    # Calculate received power for each transmission antenna
    received_powers = dict()
    received_powers[tx_antenna_1.TX_id] = metrics.received_power(tx_antenna_1.TX_gain, rx_antenna.RX_gain, tx_antenna_1.TX_power, losses["TX_1"])
    received_powers[tx_antenna_2.TX_id] = metrics.received_power(tx_antenna_2.TX_gain, rx_antenna.RX_gain, tx_antenna_2.TX_power, losses["TX_2"])
    received_powers[tx_antenna_3.TX_id] = metrics.received_power(tx_antenna_3.TX_gain, rx_antenna.RX_gain, tx_antenna_3.TX_power, losses["TX_3"])

    # Calculate the highest value and obtain the TX antenna
    antenna_principal_link = max(received_powers, key=received_powers.get)
    p_principal_link_db = received_powers[antenna_principal_link]

    # Calculate interference
    interference = 0
    for current_key in received_powers.keys():
        if current_key != antenna_principal_link:
            interference = interference + received_powers[current_key]

    # Calculate SINR
    sinr_db = metrics.calculate_sinr(p_principal_link_db, p_noise, interference)

    # Calculate link capacity
    link_capacity = metrics.capacity(bw, sinr_db)

    # Print results
    print("Link capacity: " + str(link_capacity) + " Mbps")