# Excepciones personalizadas del sistema de transporte de carga.
# Todas heredan de Exception y guardan un mensaje claro de lo que pasó.


class CargaExcedidaError(Exception):
    # Se lanza cuando la carga del viaje es mayor a la que aguanta el vehículo
    def __init__(self, placa, carga_kg, carga_maxima_kg):
        super().__init__(f"El vehículo {placa} no puede llevar {carga_kg} kg (carga máxima: {carga_maxima_kg} kg).")


class ConductorNoHabilitadoError(Exception):
    # Se lanza cuando el conductor no puede manejar ese vehículo (licencia vencida o categoría que no sirve)
    def __init__(self, nombre_conductor, motivo):
        super().__init__(f"El conductor {nombre_conductor} no está habilitado: {motivo}.")


class DocumentosVencidosError(Exception):
    # Se lanza cuando el SOAT o la revisión técnico-mecánica del vehículo están vencidos
    def __init__(self, placa, documento):
        super().__init__(f"El vehículo {placa} tiene vencido el documento: {documento}.")