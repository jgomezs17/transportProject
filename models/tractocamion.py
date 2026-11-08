# Clase Tractocamion
# Cabezote que arrastra un remolque, para carga pesada y distancias largas.
# Hereda de Vehiculo y sobrescribe el cálculo del costo, la actividad principal y ShowInformation.

from datetime import date
from models.vehiculo import Vehiculo


class Tractocamion(Vehiculo):
    TARIFA_BASE_KM = 4000        # pesos por kilómetro
    TARIFA_POR_EJE = 800         # se suma por cada eje que tenga
    CATEGORIA_LICENCIA = "C3"    # licencia mínima que pide este tipo de vehículo
    TIPOS_REMOLQUE = ["plataforma", "cisterna", "contenedor"]

    def __init__(self, placa, marca, modelo, carga_maxima_kg,
                 vencimiento_soat, vencimiento_tecnomecanica, numero_ejes, tipo_remolque):
        # lo común lo guarda Vehiculo (incluida la categoría de licencia que pide este tipo)
        super().__init__(placa, marca, modelo, carga_maxima_kg, Tractocamion.CATEGORIA_LICENCIA,
                         vencimiento_soat, vencimiento_tecnomecanica)

        # valores por defecto: si el dato es inválido avisa y queda así
        self.__numero_ejes = 0
        self.__tipo_remolque = ""

        # uso los setters para que pasen por las validaciones
        self.SetNumeroEjes(numero_ejes)
        self.SetTipoRemolque(tipo_remolque)

    # ---------- Getters ----------
    def GetNumeroEjes(self):
        return self.__numero_ejes

    def GetTipoRemolque(self):
        return self.__tipo_remolque

    # ---------- Setters con validaciones ----------
    def SetNumeroEjes(self, numero_ejes):
        # un tractocamión con remolque tiene entre 3 y 9 ejes
        if not isinstance(numero_ejes, int) or numero_ejes < 3 or numero_ejes > 9:
            print("Error: el número de ejes debe ser un entero entre 3 y 9. No se aplicó el cambio.")
            return
        self.__numero_ejes = numero_ejes

    def SetTipoRemolque(self, tipo_remolque):
        if tipo_remolque is None or str(tipo_remolque).strip().lower() not in Tractocamion.TIPOS_REMOLQUE:
            print(f"Error: el tipo de remolque debe ser uno de {Tractocamion.TIPOS_REMOLQUE}. No se aplicó el cambio.")
            return
        self.__tipo_remolque = str(tipo_remolque).strip().lower()

    # ---------- Métodos de la clase ----------
    def CalcularCostoViaje(self, distancia_km):
        if not isinstance(distancia_km, (int, float)) or distancia_km <= 0:
            print("Error: la distancia debe ser un número mayor que 0.")
            return 0
        # entre más ejes tiene, más cuesta cada kilómetro
        tarifa = Tractocamion.TARIFA_BASE_KM + Tractocamion.TARIFA_POR_EJE * self.__numero_ejes
        return distancia_km * tarifa

    def PerformMainActivity(self):
        return (f"El tractocamión {self.GetPlaca()} arrastra un remolque tipo {self.__tipo_remolque} "
                f"y mueve carga pesada a larga distancia.")

    def ShowInformation(self):
        return (super().ShowInformation() + "\n"
                f"Tipo: Tractocamión | Ejes: {self.__numero_ejes} | Remolque: {self.__tipo_remolque}")


if __name__ == "__main__":
    # Prueba rápida de la clase
    t = Tractocamion("jkl789", "Kenworth", 2019, 30000, date(2027, 5, 10), date(2027, 3, 20), 5, "Cisterna")
    print(t.ShowInformation())
    print(t.PerformMainActivity())
    print(f"Costo de 100 km: ${t.CalcularCostoViaje(100):,.0f}")

    # Datos inválidos: se informa y no se cambian
    t.SetNumeroEjes(1)
    t.SetTipoRemolque("jaula")
    t.CalcularCostoViaje(-10)