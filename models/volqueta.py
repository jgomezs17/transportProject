# Clase Volqueta
# Camión con platón basculante para llevar material de construcción.
# Hereda de Vehiculo y sobrescribe el cálculo del costo, la actividad principal y ShowInformation.

from datetime import date
from models.vehiculo import Vehiculo


class Volqueta(Vehiculo):
    TARIFA_POR_KM = 3500         # pesos por kilómetro
    CATEGORIA_LICENCIA = "C2"    # licencia mínima que pide este tipo de vehículo
    # cada material tiene un factor: el más pesado o incómodo se cobra más caro
    FACTOR_MATERIAL = {"arena": 1.0, "grava": 1.1, "escombros": 1.2}

    def __init__(self, placa, marca, modelo, carga_maxima_kg,
                 vencimiento_soat, vencimiento_tecnomecanica, tipo_material, capacidad_m3):
        # lo común lo guarda Vehiculo (incluida la categoría de licencia que pide este tipo)
        super().__init__(placa, marca, modelo, carga_maxima_kg, Volqueta.CATEGORIA_LICENCIA,
                         vencimiento_soat, vencimiento_tecnomecanica)

        # valores por defecto: si el dato es inválido avisa y queda así
        self.__tipo_material = ""
        self.__capacidad_m3 = 0

        # uso los setters para que pasen por las validaciones
        self.SetTipoMaterial(tipo_material)
        self.SetCapacidadM3(capacidad_m3)

    # ---------- Getters ----------
    def GetTipoMaterial(self):
        return self.__tipo_material

    def GetCapacidadM3(self):
        return self.__capacidad_m3

    # ---------- Setters con validaciones ----------
    def SetTipoMaterial(self, tipo_material):
        materiales = list(Volqueta.FACTOR_MATERIAL.keys())
        if tipo_material is None or str(tipo_material).strip().lower() not in materiales:
            print(f"Error: el tipo de material debe ser uno de {materiales}. No se aplicó el cambio.")
            return
        self.__tipo_material = str(tipo_material).strip().lower()

    def SetCapacidadM3(self, capacidad_m3):
        if not isinstance(capacidad_m3, (int, float)) or capacidad_m3 <= 0:
            print("Error: la capacidad debe ser un número mayor que 0. No se aplicó el cambio.")
            return
        self.__capacidad_m3 = capacidad_m3

    # ---------- Métodos de la clase ----------
    def CalcularCostoViaje(self, distancia_km):
        if not isinstance(distancia_km, (int, float)) or distancia_km <= 0:
            print("Error: la distancia debe ser un número mayor que 0.")
            return 0
        # si el material no es válido, se cobra como arena (factor 1)
        factor = Volqueta.FACTOR_MATERIAL.get(self.__tipo_material, 1.0)
        return distancia_km * Volqueta.TARIFA_POR_KM * factor

    def PerformMainActivity(self):
        return (f"La volqueta {self.GetPlaca()} transporta {self.__tipo_material} "
                f"({self.__capacidad_m3} m³) para obras y construcción.")

    def ShowInformation(self):
        return (super().ShowInformation() + "\n"
                f"Tipo: Volqueta | Material: {self.__tipo_material} | Capacidad: {self.__capacidad_m3} m³")


if __name__ == "__main__":
    # Prueba rápida de la clase
    v = Volqueta("mno321", "Chevrolet", 2018, 12000, date(2027, 1, 30), date(2027, 2, 28), "Escombros", 14)
    print(v.ShowInformation())
    print(v.PerformMainActivity())
    print(f"Costo de 100 km: ${v.CalcularCostoViaje(100):,.0f}")

    # Datos inválidos: se informa y no se cambian
    v.SetTipoMaterial("madera")
    v.SetCapacidadM3(0)
    v.CalcularCostoViaje("cien")