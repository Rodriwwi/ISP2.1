
import math as m  # Alias to rename a library
import math_utils as mu


def capacity(bw: float, snr_db: float):
    """
        Calculation of the link capacity.

        :param bw: bandwidth available per link (in MHz).
        :param snr_db: signal-to-noise ratio of the link (in dB).
        :return c: capacity of the link (Mbps).
    """

    # Shannon formula
    c = bw * m.log2(1 + mu.dbm_to_lineal_units(snr_db))

    return c


def free_space_path_losses(d: float, f: float, c: float = 3e8):
    """
        Calculation of the free space path losses between transmitter and receiver antenna.

        :param d: distance between transceiver and receiver device (in meters).
        :param f: operational frequency of the TX-RX link (in GHz).
        :param* c: speed light (in m/s). Defaults to 3e8.
        :return L: free space path losses (in dB).
    """

    L = 20 * m.log10(4 * m.pi * d * f * 10e9 / c)  # Frequency in Hz

    return L


def received_power(tx_gain: float, rx_gain: float, p_tx_db: float, losses: float):
    """
        Calculation of the receiver power (link budget).

        :param tx_gain: transmitter gain (in dBi).
        :param rx_gain: receiver gain (in dBi).
        :param p_tx_db: transmitter power (in dBm).
        :param losses: free space path losses (in dB).
        :return p_rx_db: power receiver by rx element (in dBm).
    """

    # Link budget formula
    p_rx_dbm = p_tx_db + tx_gain + rx_gain - losses

    return p_rx_dbm


def calculate_sinr(p_rx_db: float, p_noise: float, interference: float):
    """
        Calculation of the SINR. For SNR calculation -> interference = 0.

        :param p_rx_db: received power of the principal link (in dBm).
        :param p_noise: noise power of the channel (in lineal units).
        :param interference: power of the interference signals (sum of the rx power by any device with the same frequency).
        :return sinr: signal-to-interference-plus-noise-ratio (in lineal units).
    """

    sinr = mu.dbm_to_lineal_units(p_rx_db) / (p_noise + interference)

    return sinr
