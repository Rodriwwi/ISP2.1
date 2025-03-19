from transmitter_antenna import TransmitterAntenna
from rx_device import RxDevice
import metrics as me
import math_utils as mu

if __name__ == '__main__':
    # Configuración del escenario
    p_noise = 0.000002 #mW

    # Configuración del transmisor
    freqTx = 2400 # Mhz
    tx_pos = (9,1) #m
    elevation_tx = 1 #m
    bw = 20 #MHZ
    p_tx = 12 # dBm
    gain_tx = 9 #dBi

    # Configuración del repetidor
    freqRepetidor = 2400  # Mhz
    repetidor_pos = (1, 10)  # m
    elevation_repetidor = 1  # m
    bwRepetidor = 20  # MHZ
    p_repetidor = 10  # dBm
    gain_repetidor = 3  # dBi

    # Configuración del móvil
    pos_movil = (6,3) #m
    elevation_movil = 1.5 #m
    gain_movil = 1 #dBi

    # Configuración de la tablet
    pos_tablet = (4, 5)  # m
    elevation_tablet = 1.5  # m
    gain_tablet = 2  # dBi

    #RX Configuration
    rx_pos_movil = (6,3)
    gain_rx = 1
    rx_pos_tablet = (4,5)
    gain_rx_tablet = 2
    elevation_rx = 1.5


    # Instanciación de objetos
    transmisor = TransmitterAntenna("TX_1",tx_pos,elevation_tx,bw,freqTx/1000,p_tx,gain_tx)
    repetidor = TransmitterAntenna("REPE",repetidor_pos,elevation_repetidor,bwRepetidor,freqRepetidor/1000,p_repetidor,gain_repetidor)
    movil = RxDevice("movil",pos_movil,elevation_movil,gain_movil,transmisor.TX_bandwidth/2)
    tablet = RxDevice("tablet",pos_tablet,elevation_tablet,gain_tablet,transmisor.TX_bandwidth/2)

    #Lógica
    # en el movil
    distancia_TX1_movil = mu.calculate_distance(transmisor.TX_position, movil.RX_position)
    distancia_TX2_movil = mu.calculate_distance(repetidor.TX_position, movil.RX_position)
    distancia_TX1_tablet = mu.calculate_distance(transmisor.TX_position, tablet.RX_position)
    distancia_TX2_tablet = mu.calculate_distance(repetidor.TX_position, tablet.RX_position)

    # FSPL
    free_space_path_loss_TX_movil = me.free_space_path_losses(distancia_TX1_movil, transmisor.TX_frequency)
    print("Pérdidas en espacio libre entre el TX y el móvil: " + str(free_space_path_loss_TX_movil) + " dB")
    free_space_path_loss_repe_movil = me.free_space_path_losses(distancia_TX2_movil, transmisor.TX_frequency)
    print("Pérdidas en espacio libre entre el repetidor y el móvil: " + str(free_space_path_loss_repe_movil) + " dB")
    free_space_path_loss_TX_tablet = me.free_space_path_losses(distancia_TX1_tablet, repetidor.TX_frequency)
    print("Pérdidas en espacio libre entre el TX y la tablet: " + str(free_space_path_loss_TX_tablet) + " dB")
    free_space_path_loss_repe_tablet = me.free_space_path_losses(distancia_TX2_tablet, repetidor.TX_frequency)
    print("Pérdidas en espacio libre entre el repetidor y la tablet: " + str(free_space_path_loss_repe_movil) + " dB")


    # Potencia recibida.

    rx_power_movil_tx2 = me.received_power(transmisor.TX_gain, movil.RX_gain, transmisor.TX_power, free_space_path_loss_TX_movil)
    rx_power_movil_tx2 = me.
    # en la tablet
    distancia_TX_tablet = mu.calculate_distance(transmisor.TX_position, tablet.RX_position)
    print("Distancia TX-Tablet: " + str(distancia_TX_tablet) + "m")

    free_space_path_loss_TX_tablet = me.free_space_path_losses(distancia_TX_tablet, transmisor.TX_frequency)
    print("Pérdidas en espacio libre entre el TX y la tablet: " + str(free_space_path_loss_TX_tablet) + " dB")

    received_power_tablet = me.received_power(transmisor.TX_gain, tablet.RX_gain, transmisor.TX_power,free_space_path_loss_TX_tablet)
    tablet.RX_power = received_power_tablet
    print("Potencia recibida por la tablet: " + str(movil.RX_power) + " mW")

    signal_to_noise_ratio_movil = me.calculate_sinr(received_power_movil, p_noise, tablet.RX_power)
    print("SINR: " + str(signal_to_noise_ratio_movil))

    movil.RX_bandwidth = transmisor.TX_bandwidth/2
    tablet.RX_bandwidth = transmisor.TX_bandwidth/2

    db_snr = mu.lineal_units_to_dbm(signal_to_noise_ratio_movil)
    capacity = me.capacity(movil.RX_bandwidth, db_snr)
    print("Capacidad del enlace TX-Móvil: " + str(capacity * 10e6) + " bps")



