# Clase CamionFurgon
# Camión con furgón cerrado para llevar mercancía empacada.
# Hereda de Vehiculo y sobrescribe el cálculo del costo, la actividad principal y ShowInformation.

from datetime import date
from models.vehiculo import Vehiculo


class CamionFurgon(Vehiculo):
    TARIFA_POR_KM = 3000         # pesos por kilómetro
    RECARGO_REFRIGERADO = 1.25   # si va refrigerado se cobra 25% más
    CATEGORIA_LICENCIA = "C2"    # licencia mínima que pide este tipo de vehículo

    def __init__(self, placa, marca, modelo, carga_maxima_kg,
                 vencimiento_soat, vencimiento_tecnomecanica, volumen_m3, refrigerado):
        # lo común lo guarda Vehiculo (incluida la categoría de licencia que pide este tipo)
        super().__init__(placa, marca, modelo, carga_maxima_kg, CamionFurgon.CATEGORIA_LICENCIA,
                         vencimiento_soat, vencimiento_tecnomecanica)

        # valores por defecto: si el dato es inválido avisa y queda así
        self.__volumen_m3 = 0
        self.__refrigerado = False

        # uso los setters para que pasen por las validaciones
        self.SetVolumenM3(volumen_m3)
        self.SetRefrigerado(refrigerado)

    # ---------- Getters ----------
    def GetVolumenM3(self):
        return self.__volumen_m3

    def GetRefrigerado(self):
        return self.__refrigerado

    # ---------- Setters con validaciones ----------
    def SetVolumenM3(self, volumen_m3):
        if not isinstance(volumen_m3, (int, float)) or volumen_m3 <= 0:
            print("Error: el volumen debe ser un número mayor que 0. No se aplicó el cambio.")
            return
        self.__volumen_m3 = volumen_m3

    def SetRefrigerado(self, refrigerado):
        # tiene que ser True o False, no un texto
        if not isinstance(refrigerado, bool):
            print("Error: refrigerado debe ser True o False. No se aplicó el cambio.")
            return
        self.__refrigerado = refrigerado

    # ---------- Métodos de la clase ----------
    def CalcularCostoViaje(self, distancia_km):
        if not isinstance(distancia_km, (int, float)) or distancia_km <= 0:
            print("Error: la distancia debe ser un número mayor que 0.")
            return 0
        costo = distancia_km * CamionFurgon.TARIFA_POR_KM
        # el furgón refrigerado gasta más, por eso se cobra un recargo
        if self.__refrigerado:
            costo = costo * CamionFurgon.RECARGO_REFRIGERADO
        return costo

    def PerformMainActivity(self):
        tipo = "refrigerado" if self.__refrigerado else "seco"
        return (f"El camión {self.GetPlaca()} transporta mercancía empacada en un furgón "
                f"{tipo} de {self.__volumen_m3} m³.")

    def ShowInformation(self):
        refrigerado = "Sí" if self.__refrigerado else "No"
        return (super().ShowInformation() + "\n"
                f"Tipo: Camión furgón | Volumen: {self.__volumen_m3} m³ | Refrigerado: {refrigerado}")


if __name__ == "__main__":
    # Prueba rápida de la clase
    f = CamionFurgon("fgh456", "Hino", 2021, 6000, date(2027, 4, 1), date(2027, 2, 15), 30, True)
    print(f.ShowInformation())
    print(f.PerformMainActivity())
    print(f"Costo de 100 km: ${f.CalcularCostoViaje(100):,.0f}")

    # Datos inválidos: se informa y no se cambian
    f.SetVolumenM3(-4)
    f.SetRefrigerado("si")
    f.CalcularCostoViaje(0)