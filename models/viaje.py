# Clase Viaje
# Un viaje de carga: sale de un origen a un destino, con un vehículo y un conductor.
# Relaciona objetos Vehiculo y Conductor (asociación). Al programarlo se revisa que
# la carga, los documentos y la licencia estén bien, y si algo falla se lanza la excepción.

from datetime import date
from models.vehiculo import Vehiculo
from models.conductor import Conductor


class Viaje:
    def __init__(self, codigo, origen, destino, distancia_km, carga_kg, vehiculo, conductor):
        # valores vacíos por defecto: si el dato es inválido avisa y queda vacío
        self.__codigo = ""
        self.__origen = ""
        self.__destino = ""
        self.__distancia_km = 0
        self.__carga_kg = 0
        # se guardan los objetos completos (asociación), no solo la placa o el nombre
        self.__vehiculo = None
        self.__conductor = None
        # todo viaje empieza pendiente y pasa a programado cuando pasa las verificaciones
        self.__estado = "pendiente"
        self.__fecha = None

        # uso los setters para que pasen por las validaciones
        self.SetCodigo(codigo)
        self.SetOrigen(origen)
        self.SetDestino(destino)
        self.SetDistanciaKm(distancia_km)
        self.SetCargaKg(carga_kg)
        self.SetVehiculo(vehiculo)
        self.SetConductor(conductor)

    # ---------- Getters ----------
    def GetCodigo(self):
        return self.__codigo

    def GetOrigen(self):
        return self.__origen

    def GetDestino(self):
        return self.__destino

    def GetDistanciaKm(self):
        return self.__distancia_km

    def GetCargaKg(self):
        return self.__carga_kg

    def GetVehiculo(self):
        return self.__vehiculo

    def GetConductor(self):
        return self.__conductor

    def GetEstado(self):
        return self.__estado

    def GetFecha(self):
        return self.__fecha

    # ---------- Setters con validaciones ----------
    def SetCodigo(self, codigo):
        if codigo is None or str(codigo).strip() == "":
            print("Error: el código del viaje no puede estar vacío. No se aplicó el cambio.")
            return
        self.__codigo = str(codigo).strip()

    def SetOrigen(self, origen):
        if origen is None or str(origen).strip() == "":
            print("Error: el origen no puede estar vacío. No se aplicó el cambio.")
            return
        self.__origen = str(origen).strip()

    def SetDestino(self, destino):
        if destino is None or str(destino).strip() == "":
            print("Error: el destino no puede estar vacío. No se aplicó el cambio.")
            return
        self.__destino = str(destino).strip()

    def SetDistanciaKm(self, distancia_km):
        if not isinstance(distancia_km, (int, float)) or distancia_km <= 0:
            print("Error: la distancia debe ser un número mayor que 0. No se aplicó el cambio.")
            return
        self.__distancia_km = distancia_km

    def SetCargaKg(self, carga_kg):
        if not isinstance(carga_kg, (int, float)) or carga_kg <= 0:
            print("Error: la carga debe ser un número mayor que 0. No se aplicó el cambio.")
            return
        self.__carga_kg = carga_kg

    def SetVehiculo(self, vehiculo):
        # tiene que ser un objeto Vehiculo (una de sus hijas), no un texto suelto
        if not isinstance(vehiculo, Vehiculo):
            print("Error: el vehículo debe ser un objeto Vehiculo. No se aplicó el cambio.")
            return
        self.__vehiculo = vehiculo

    def SetConductor(self, conductor):
        # tiene que ser un objeto Conductor, no un texto suelto
        if not isinstance(conductor, Conductor):
            print("Error: el conductor debe ser un objeto Conductor. No se aplicó el cambio.")
            return
        self.__conductor = conductor

    # ---------- Métodos de la clase ----------
    def Programar(self, fecha):
        if not isinstance(fecha, date):
            print("Error: la fecha del viaje debe ser una fecha. No se programó el viaje.")
            return
        if self.__vehiculo is None or self.__conductor is None:
            print("Error: el viaje necesita un vehículo y un conductor para programarse.")
            return
        # cada verificación lanza su excepción si algo está mal, y entonces el viaje
        # se queda pendiente porque nunca llega a la última línea
        self.__vehiculo.ValidarCarga(self.__carga_kg)
        self.__vehiculo.VerificarDocumentos(fecha)
        self.__conductor.VerificarHabilitacion(self.__vehiculo.GetCategoriaLicencia(), fecha)
        self.__estado = "programado"
        self.__fecha = fecha
        print(f"Viaje {self.__codigo} programado para el {fecha}.")

    def CalcularCosto(self):
        if self.__vehiculo is None:
            return 0
        # cada tipo de vehículo calcula el costo a su manera
        return self.__vehiculo.CalcularCostoViaje(self.__distancia_km)

    def ShowInformation(self):
        placa = self.__vehiculo.GetPlaca() if self.__vehiculo is not None else ""
        conductor = self.__conductor.GetNombre() if self.__conductor is not None else ""
        fecha = str(self.__fecha) if self.__fecha is not None else "sin programar"
        return (f"Viaje: {self.__codigo} | {self.__origen} -> {self.__destino}\n"
                f"Distancia: {self.__distancia_km} km | Carga: {self.__carga_kg} kg\n"
                f"Vehículo: {placa} | Conductor: {conductor}\n"
                f"Estado: {self.__estado} | Fecha: {fecha} | Costo estimado: ${self.CalcularCosto():,.0f}")


if __name__ == "__main__":
    # Prueba rápida de la clase
    from models.volqueta import Volqueta
    from exceptions.excepciones import CargaExcedidaError

    volqueta = Volqueta("mno321", "Chevrolet", 2018, 12000, date(2027, 1, 30), date(2027, 2, 28), "arena", 14)
    conductor = Conductor("Luis Ortiz", "1010", "LIC-001", "C2", date(2028, 5, 20))

    viaje = Viaje("V001", "Bogotá", "Tunja", 150, 9000, volqueta, conductor)
    print(viaje.ShowInformation())
    viaje.Programar(date(2026, 11, 8))
    print(viaje.ShowInformation())

    # Datos inválidos: se informa y no se cambian
    viaje.SetDistanciaKm(-5)
    viaje.SetVehiculo("MNO321")

    # Carga mayor a la que aguanta la volqueta: se lanza la excepción
    viaje2 = Viaje("V002", "Bogotá", "Cali", 460, 20000, volqueta, conductor)
    try:
        viaje2.Programar(date(2026, 11, 8))
    except CargaExcedidaError as error:
        print(f"Error: {error}")
    print(f"Estado del viaje V002: {viaje2.GetEstado()}")
