from transmitter_antenna import TransmitterAntenna
from rx_device import RxDevice
import metrics as me
import math_utils as mu

if __name__ == '__main__':
    # Configuración del escenario
    p_noise = mu.dbm_to_lineal_units(-60)  # mW

    # Transmisores
    tx_1 = TransmitterAntenna("TX_1", (30, 80), 7, 10, 2.4, 17, 4)
    tx_2 = TransmitterAntenna("TX_2", (20, 30), 7, 7, 6, 19, 9)
    tx_3 = TransmitterAntenna("TX_3", (50, 90), 7, 20, 6, 20, 5)
    tx_4 = TransmitterAntenna("TX_4", (65, 70), 7, 10, 2.4, 17, 2)
    tx_5 = TransmitterAntenna("TX_5", (60, 40), 7, 12, 2.4, 21, 8)
    tx_6 = TransmitterAntenna("TX_6", (40, 65), 7, 20, 6, 18, 9)
    vector_transmisores = [tx_1, tx_2, tx_3, tx_4, tx_5, tx_6]

    # Receptores
    rx_1 = RxDevice("RX_1", (30, 80), 1.5, 5, 0)
    rx_2 = RxDevice("RX_2", (55, 80), 1.5, 5, 0)
    rx_3 = RxDevice("RX_1", (45, 45), 1.5, 5, 0)
    vector_receptores = [rx_1, rx_2, rx_3]

    # Conectar todos los receptores al TX6
    vector_transmisores[5].connected_devices.append(tx_1.TX_id)
    rx_1.RX_bandwidth = vector_transmisores[5].TX_bandwidth / len(vector_transmisores[5].connected_devices)  # Repartimos el ancho de banda

    vector_transmisores[5].connected_devices.append(tx_2.TX_id)
    rx_2.RX_bandwidth = vector_transmisores[5].TX_bandwidth / len(vector_transmisores[5].connected_devices)  # Repartimos el ancho de banda

    vector_transmisores[5].connected_devices.append(tx_3.TX_id)
    rx_3.RX_bandwidth = vector_transmisores[5].TX_bandwidth / len(vector_transmisores[5].connected_devices)  # Repartimos el ancho de banda

    # Presupuesto de potencia
    d_e1 = mu.calculate_distance(vector_transmisores[5].TX_position, rx_1.RX_position)
    losses_e1 = me.free_space_path_losses(d_e1, vector_transmisores[5].TX_frequency)
    p_signal_e1 = me.received_power(vector_transmisores[5].TX_gain, rx_1.RX_gain, vector_transmisores[5].TX_power,losses_e1)

    # Calcular interferencia
    p_int = 0

    for i in range(0, len(vector_transmisores) - 1):
        if vector_transmisores[i].TX_frequency == vector_transmisores[5].TX_frequency:
            d_aux = mu.calculate_distance(vector_transmisores[i].TX_position, rx_1.RX_position)
            losses_aux = me.free_space_path_losses(d_aux, vector_transmisores[i].TX_frequency)
            p_signal_aux_dbm = me.received_power(vector_transmisores[i].TX_gain, rx_1.RX_gain,vector_transmisores[i].TX_power, losses_aux)
            p_int += mu.dbm_to_lineal_units(p_signal_aux_dbm)

    # Calcular capacidad
    sinr_e1 = me.calculate_sinr(p_signal_e1, mu.dbm_to_lineal_units(p_noise), p_int)
    c_e1 = me.capacity(rx_1.RX_bandwidth, mu.dbm_to_lineal_units(sinr_e1))


    #Transmisor 2
    # Presupuesto de potencia
    d_e2 = mu.calculate_distance(vector_transmisores[5].TX_position, rx_2.RX_position)
    losses_e2 = me.free_space_path_losses(d_e2, vector_transmisores[5].TX_frequency)
    p_signal_e2 = me.received_power(vector_transmisores[5].TX_gain, rx_2.RX_gain, vector_transmisores[5].TX_power,
                                    losses_e2)

    # Calcular interferencia
    p_int_2 = 0

    for i in range(0, len(vector_transmisores) - 1):
        if vector_transmisores[i].TX_frequency == vector_transmisores[5].TX_frequency:
            d_aux = mu.calculate_distance(vector_transmisores[i].TX_position, rx_2.RX_position)
            losses_aux = me.free_space_path_losses(d_aux, vector_transmisores[i].TX_frequency)
            p_signal_aux_dbm = me.received_power(vector_transmisores[i].TX_gain, rx_2.RX_gain,
                                                 vector_transmisores[i].TX_power, losses_aux)
            p_int_2 += mu.dbm_to_lineal_units(p_signal_aux_dbm)

    # Calcular capacidad
    sinr_e2 = me.calculate_sinr(p_signal_e2, mu.dbm_to_lineal_units(p_noise), p_int_2)
    c_e2 = me.capacity(rx_2.RX_bandwidth, mu.dbm_to_lineal_units(sinr_e2))


    print("Capacidad del enlace TX-RX 1: " + str(c_e1) + " Mbps")
    print("Capacidad del enlace TX-RX 2: " + str(c_e2) + " Mbps")


    #todo calcular capacidad del transmisor 3 pero el cálculo de la sinr tiene que ser obligatoriamente calculado de otra manera.
    # por ejemplo crear un atributo en la clase receptor -string- identificado del transmisor, para calcular la interferencia recorrer todos los transmisores
    # hasta el último con un for --> hacer if tx_id == rx_id calcular la potencia y meter como :
    # freq_aux = (hacer prerrecorrido)
    #   freq_aux = vector_tx[5].tx_freq
    # .
    # .
    # for i in range(0,len(vector_tx)):
    #   if vector_tx[i].tx_id == rx_3.connected_tx:
    #       p_señal = calcular_rx_power
    #   else:
    #       if vector_tx[i].tx_freq == freq_aux:
    #       p_intereferencia = calcular_rx_power