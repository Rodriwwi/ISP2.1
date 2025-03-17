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
    repetidor_pos = (9, 1)  # m
    elevation_repetidor = 1  # m
    bwRepetidor = 20  # MHZ
    p_repetidor = 10  # dBm
    gain_repetidor = 3  # dBi

    # Configuración del móvil
    pos_movil = (7,3) #m
    elevation_movil = 1.5 #m
    gain_movil = 5 #dBi

    # Configuración de la tablet
    pos_tablet = (4, 5)  # m
    elevation_tablet = 1.5  # m
    gain_tablet = 5  # dBi

    # Instanciación de objetos
    transmisor = TransmitterAntenna("TX_1",tx_pos,elevation_tx,bw,freqTx,p_tx,gain_tx)
    repetidor = TransmitterAntenna("REPE",repetidor_pos,elevation_repetidor,bwRepetidor,freqRepetidor,p_repetidor,gain_repetidor)
    movil = RxDevice("movil",pos_movil,elevation_movil,gain_movil,transmisor.TX_bandwidth/2)
    tablet = RxDevice("tablet",pos_tablet,elevation_tablet,gain_tablet,transmisor.TX_bandwidth/2)

    #Lógica

    # en el movil
    distancia_TX_movil = mu.calculate_distance(transmisor.TX_position, movil.RX_position)
    print("Distancia TX-Móvil: " + str(distancia_TX_movil) + "m")

    free_space_path_loss_TX_movil = me.free_space_path_losses(distancia_TX_movil, transmisor.TX_frequency)
    print("Pérdidas en espacio libre entre el TX y el móvil: " + str(free_space_path_loss_TX_movil) + " dB")

    received_power_movil = me.received_power(transmisor.TX_gain, movil.RX_gain, transmisor.TX_power, free_space_path_loss_TX_movil)
    movil.RX_power = received_power_movil
    print("Potencia recibida por el móvil: " + str(movil.RX_power) + " mW")

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



