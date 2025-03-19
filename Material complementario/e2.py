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

    #Distancias
    distancia_TX1_movil = mu.calculate_distance(transmisor.TX_position, movil.RX_position)
    distancia_TX2_movil = mu.calculate_distance(repetidor.TX_position, movil.RX_position)
    distancia_TX1_tablet = mu.calculate_distance(transmisor.TX_position, tablet.RX_position)
    distancia_TX2_tablet = mu.calculate_distance(repetidor.TX_position, tablet.RX_position)

    #FSPL
    free_space_path_loss_TX_movil = me.free_space_path_losses(distancia_TX1_movil, transmisor.TX_frequency)
    print("Pérdidas en espacio libre entre el TX y el móvil: " + str(free_space_path_loss_TX_movil) + " dB")
    free_space_path_loss_repe_movil = me.free_space_path_losses(distancia_TX2_movil, transmisor.TX_frequency)
    print("Pérdidas en espacio libre entre el repetidor y el móvil: " + str(free_space_path_loss_repe_movil) + " dB")
    free_space_path_loss_TX_tablet = me.free_space_path_losses(distancia_TX1_tablet, repetidor.TX_frequency)
    print("Pérdidas en espacio libre entre el TX y la tablet: " + str(free_space_path_loss_TX_tablet) + " dB")
    free_space_path_loss_repe_tablet = me.free_space_path_losses(distancia_TX2_tablet, repetidor.TX_frequency)
    print("Pérdidas en espacio libre entre el repetidor y la tablet: " + str(free_space_path_loss_repe_movil) + " dB")


    # Asignación del movil
    rx_power_movil_tx1 = me.received_power(transmisor.TX_gain, movil.RX_gain, transmisor.TX_power, free_space_path_loss_TX_movil)
    rx_power_movil_tx2 = me.received_power(repetidor.TX_gain, movil.RX_gain, repetidor.TX_power, free_space_path_loss_repe_movil)

    if rx_power_movil_tx1 > rx_power_movil_tx2:
        movil.RX_power = rx_power_movil_tx1
        transmisor.connected_devices.append(tablet.RX_id)
        interference = rx_power_movil_tx2
    else:
        movil.RX_power = rx_power_movil_tx2
        repetidor.connected_devices.append(tablet.RX_id)
        interference = rx_power_movil_tx1

    # Asignación de la tablet
    rx_power_tablet_tx1 = me.received_power(transmisor.TX_gain, tablet.RX_gain, transmisor.TX_power,free_space_path_loss_TX_tablet)
    rx_power_tablet_tx2 = me.received_power(repetidor.TX_gain, tablet.RX_gain, repetidor.TX_power, free_space_path_loss_repe_tablet)

    if rx_power_tablet_tx1 > rx_power_tablet_tx2:
        tablet.RX_power = rx_power_tablet_tx1
        transmisor.connected_devices.append(tablet.RX_id)
    else:
        tablet.RX_power = rx_power_tablet_tx2
        repetidor.connected_devices.append(tablet.RX_id)


    # SINR
    snr_movil = me.calculate_sinr(movil.RX_power, p_noise, interference)
    #print("SINR movil: "+str(snr_movil))
    snr_tablet = me.calculate_sinr(tablet.RX_power, p_noise, interference)
    #print("SINR tablet: "+str(snr_tablet))

    # Capacidad y asignación de ancho de banda
    if movil.RX_id in transmisor.connected_devices:
        movil.RX_bandwidth = transmisor.TX_bandwidth / len(transmisor.connected_devices)
    elif movil.RX_id in repetidor.connected_devices:
        movil.RX_bandwidth = repetidor.TX_bandwidth / len(repetidor.connected_devices)

    if tablet.RX_id in transmisor.connected_devices:
        tablet.RX_bandwidth = transmisor.TX_bandwidth / len(transmisor.connected_devices)
    elif tablet.RX_id in repetidor.connected_devices:
        tablet.RX_bandwidth = repetidor.TX_bandwidth / len(repetidor.connected_devices)

    capacity_movil = me.capacity(movil.RX_bandwidth,mu.dbm_to_lineal_units(snr_movil))
    print("Capacidad del enlace TX-RX movil :" + str(capacity_movil) + " Mbps")
    capacity_tablet = me.capacity(tablet.RX_bandwidth,mu.dbm_to_lineal_units(snr_tablet))
    print("Capacidad del enlace eTX-RX tablet :" + str(capacity_movil) + " Mbps")

    print(transmisor.connected_devices)

