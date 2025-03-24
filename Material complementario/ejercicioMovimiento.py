from transmitter_antenna import TransmitterAntenna
from rx_device import RxDevice
import metrics as me
import math_utils as mu

if __name__ == '__main__':

    # Scenario initial configuration
    p_noise = mu.dbm_to_lineal_units(-70) # mW

    # Object instance
    tx_1 = TransmitterAntenna("TX_1", (20,180), 12, 6, 1.95, 18, 9)
    tx_2 = TransmitterAntenna("TX_2", (180,190), 12, 6,1.95, 18, 9)
    tx_3 = TransmitterAntenna("TX_3", (180,20), 12, 6, 1.95, 18, 9)
    vector_transmisores = [tx_1, tx_2, tx_3]

    vector_posiciones = [(135,45), (100,100), (40,170)]
    rx_1 = RxDevice("RX_1", (150,20), 1.5, 2, 0, vector_posiciones)

    print("Devices initializated")
    print("")

    for i in range(0, len(rx_1.RX_steps)):

        rx_1.RX_position = rx_1.RX_steps[i]
        print("Position: " + str(rx_1.RX_position))

        dist = [0, 0, 0]
        losses = [0, 0, 0]
        received_power_mw = [0, 0, 0]

        # ! Calculate link budgets
        for j in range(0, len(vector_transmisores)):
            dist[j] = mu.calculate_distance(vector_transmisores[j].TX_position, rx_1.RX_position)
            losses[j] = me.free_space_path_losses(dist[j], vector_transmisores[j].TX_frequency)
            received_power_mw[j] = mu.dbm_to_lineal_units(me.received_power(vector_transmisores[j].TX_gain, rx_1.RX_gain, vector_transmisores[j].TX_power, losses[j]))

        # ! Connect
        pos_vector_connectado = received_power_mw.index(max(received_power_mw))
        transmisor_conectado = vector_transmisores[pos_vector_connectado].TX_id
        print("Conneted TX: " + transmisor_conectado)

        if transmisor_conectado != rx_1.connected_TX:
            rx_1.connected_TX = transmisor_conectado
            del vector_transmisores[pos_vector_connectado].connected_devices

        rx_1.RX_power = mu.lineal_units_to_dbm(received_power_mw[pos_vector_connectado])
        rx_1.RX_bandwidth = vector_transmisores[pos_vector_connectado].TX_bandwidth

        if len(vector_transmisores[pos_vector_connectado].connected_devices) == 0:
            vector_transmisores[pos_vector_connectado].connected_devices.append(rx_1.RX_id)

        # * Calculate interference
        p_interf = 0
        for i in range(0, len(vector_transmisores)):

            if pos_vector_connectado == i:
                p_signal = received_power_mw[i]

            else:
                p_interf += received_power_mw[i]

        # ! Calculate capacity
        sinr = me.calculate_sinr(mu.lineal_units_to_dbm(p_signal), p_noise, p_interf)
        c = me.capacity(rx_1.RX_bandwidth, mu.lineal_units_to_dbm(sinr))
        print("Capacity: " + str(c) + " Mbps")

        print("==================================")



        #todo en el mismo escenario del ejercicio del examen vamos a mover solo uno de los 3 transmisores (el 1 x ejemplo), cuidado con los bw
        # y vamos a mover el transmisor 1 a las posiciones (30,80),(80,80),(30,20),(80,20) y (80,50). Al hacerlo cuidado con las asignacones de ancho de banda x q ya hay 2 di
        # spotivisos que están quietos. Cuidado tambien con la interferencia xq en cada salto se puede conectar a diferentes tranmisopres que quizas operan a diferente frecuencia y
        # no considerarse como  interfecrencia.-
