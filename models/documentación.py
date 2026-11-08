# Clase Documentacion
# Guarda las fechas de vencimiento del SOAT y de la revisión técnico-mecánica.
# Se crea desde Vehiculo (composición): si no hay vehículo, no hay documentación.

from datetime import date
from exceptions.excepciones import DocumentosVencidosError


class Documentacion:
    def __init__(self, vencimiento_soat, vencimiento_tecnomecanica):
        # valores vacíos por defecto: si el dato es inválido avisa y queda vacío
        self.__vencimiento_soat = None
        self.__vencimiento_tecnomecanica = None

        # uso los setters para que pasen por las validaciones
        self.SetVencimientoSoat(vencimiento_soat)
        self.SetVencimientoTecnomecanica(vencimiento_tecnomecanica)

    # Get y Set del SOAT
    def GetVencimientoSoat(self):
        return self.__vencimiento_soat

    def SetVencimientoSoat(self, vencimiento_soat):
        # tiene que ser una fecha (date), no un texto suelto
        if not isinstance(vencimiento_soat, date):
            print("Error: el vencimiento del SOAT debe ser una fecha. No se aplicó el cambio.")
            return
        self.__vencimiento_soat = vencimiento_soat

    # Get y Set de la revisión técnico-mecánica
    def GetVencimientoTecnomecanica(self):
        return self.__vencimiento_tecnomecanica

    def SetVencimientoTecnomecanica(self, vencimiento_tecnomecanica):
        if not isinstance(vencimiento_tecnomecanica, date):
            print("Error: el vencimiento de la revisión técnico-mecánica debe ser una fecha. No se aplicó el cambio.")
            return
        self.__vencimiento_tecnomecanica = vencimiento_tecnomecanica

    def VerificarVigencia(self, fecha, placa):
        # compara cada documento con la fecha del viaje; si alguno ya venció lanza la excepción
        if self.__vencimiento_soat is None or self.__vencimiento_soat < fecha:
            raise DocumentosVencidosError(placa, "SOAT")
        if self.__vencimiento_tecnomecanica is None or self.__vencimiento_tecnomecanica < fecha:
            raise DocumentosVencidosError(placa, "revisión técnico-mecánica")

    def ShowInformation(self):
        soat = str(self.__vencimiento_soat) if self.__vencimiento_soat is not None else "sin registrar"
        tecno = str(self.__vencimiento_tecnomecanica) if self.__vencimiento_tecnomecanica is not None else "sin registrar"
        return f"SOAT vence: {soat} | Revisión técnico-mecánica vence: {tecno}"


if __name__ == "__main__":
    # Prueba rápida de la clase
    docs = Documentacion(date(2027, 3, 15), date(2026, 12, 1))
    print(docs.ShowInformation())

    # Con esta fecha todo está vigente
    docs.VerificarVigencia(date(2026, 11, 8), "ABC123")
    print("Documentos vigentes")

    # Con esta fecha la revisión técnico-mecánica ya venció
    try:
        docs.VerificarVigencia(date(2027, 1, 10), "ABC123")
    except DocumentosVencidosError as error:
        print(f"Error: {error}")

    # Dato inválido: se informa y no se cambia
    docs.SetVencimientoSoat("2027-03-15")
