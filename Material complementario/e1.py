from transmitter_antenna import TransmitterAntenna
from rx_device import RxDevice
import metrics as me
import math_utils as mu

if __name__ == '__main__':
    # Configuración del escenario
    p_noise = 0.02 #mW

    # Configuración del transmisor
    freq = 700 # Mhz
    tx_pos = (20,70) #m
    elevation_tx = 10 #m
    bw = 20 #MHZ
    p_tx = 12 # dBm
    gain_tx = 9 #dBi

    # Configuración del receptor
    rx_pos = (600,300) #m
    elevation_rx = 1.5 #m
    gain_rx = 5 #dBi

    # Object instance
    tx_1 = TransmitterAntenna("TX_1",tx_pos, elevation_tx,bw,freq/1000,p_tx,gain_tx)
    rx_1 = RxDevice("RX_1",rx_pos, elevation_rx,gain_rx,0)

    # Logica
    distance_TX_RX = mu.calculate_distance(tx_1.TX_position,rx_1.RX_position)
    print("Distancia TX-RX: " + str(distance_TX_RX) + "m")

    free_space_path_loss = me.free_space_path_losses(distance_TX_RX,tx_1.TX_frequency)
    print("Pérdidas en espacio libre: " + str(free_space_path_loss) + " dB")

    received_power = me.received_power(tx_1.TX_gain,rx_1.RX_gain,tx_1.TX_power,free_space_path_loss)
    rx_1.RX_power=received_power
    print("Potencia recibida por el receptor: "+ str(rx_1.RX_power)+" dBm")

    signal_to_noise_ratio = me.calculate_sinr(received_power,p_noise,0)
    print("SNR: "+ str(signal_to_noise_ratio))

    rx_1.RX_bandwidth = tx_1.TX_bandwidth
    db_snr = mu.lineal_units_to_dbm(signal_to_noise_ratio)
    capacity = me.capacity(rx_1.RX_bandwidth,db_snr)
    print("Capacidad del enlace TX-RX: "+ str(capacity*10e6) + " bps")



