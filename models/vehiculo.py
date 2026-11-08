# Clase Vehiculo
# Clase padre de CamionFurgon, Tractocamion y Volqueta. Es abstracta:
# no se puede crear un Vehiculo directamente, solo sus hijas.
# Aquí van los datos que tienen en común los tres tipos de vehículo.

from abc import ABC, abstractmethod
from datetime import date
from models.documentacion import Documentacion
from exceptions.excepciones import CargaExcedidaError


class Vehiculo(ABC):
    # categorías de licencia que acepto, de menor a mayor (las mismas de Conductor)
    CATEGORIAS = ["C1", "C2", "C3"]

    def __init__(self, placa, marca, modelo, carga_maxima_kg, categoria_licencia,
                 vencimiento_soat, vencimiento_tecnomecanica):
        # valores vacíos por defecto, igual que en Persona: si el dato es inválido avisa y queda vacío
        self._placa = ""
        self._marca = ""
        self._modelo = 0
        self._carga_maxima_kg = 0
        self._categoria_licencia = ""

        # uso los setters para que pasen por las validaciones
        self.SetPlaca(placa)
        self.SetMarca(marca)
        self.SetModelo(modelo)
        self.SetCargaMaximaKg(carga_maxima_kg)
        self.SetCategoriaLicencia(categoria_licencia)

        # composición: el vehículo crea su propia documentación, no la recibe ya hecha
        self._documentacion = Documentacion(vencimiento_soat, vencimiento_tecnomecanica)

    # ---------- Getters ----------
    def GetPlaca(self):
        return self._placa

    def GetMarca(self):
        return self._marca

    def GetModelo(self):
        return self._modelo

    def GetCargaMaximaKg(self):
        return self._carga_maxima_kg

    def GetCategoriaLicencia(self):
        return self._categoria_licencia

    def GetDocumentacion(self):
        return self._documentacion

    # ---------- Setters con validaciones ----------
    def SetPlaca(self, placa):
        if placa is None or str(placa).strip() == "":
            print("Error: la placa no puede estar vacía. No se aplicó el cambio.")
            return
        self._placa = str(placa).strip().upper()

    def SetMarca(self, marca):
        if marca is None or str(marca).strip() == "":
            print("Error: la marca no puede estar vacía. No se aplicó el cambio.")
            return
        self._marca = str(marca).strip()

    def SetModelo(self, modelo):
        # el modelo es el año del vehículo; no puede ser de un año futuro (más de uno)
        if not isinstance(modelo, int) or modelo < 1980 or modelo > date.today().year + 1:
            print("Error: el modelo debe ser un año válido (entero desde 1980). No se aplicó el cambio.")
            return
        self._modelo = modelo

    def SetCargaMaximaKg(self, carga_maxima_kg):
        if not isinstance(carga_maxima_kg, (int, float)) or carga_maxima_kg <= 0:
            print("Error: la carga máxima debe ser un número mayor que 0. No se aplicó el cambio.")
            return
        self._carga_maxima_kg = carga_maxima_kg

    def SetCategoriaLicencia(self, categoria_licencia):
        if categoria_licencia is None or str(categoria_licencia).strip().upper() not in Vehiculo.CATEGORIAS:
            print(f"Error: la categoría debe ser una de {Vehiculo.CATEGORIAS}. No se aplicó el cambio.")
            return
        self._categoria_licencia = str(categoria_licencia).strip().upper()

    # ---------- Métodos de la clase ----------
    def ValidarCarga(self, carga_kg):
        # si la carga del viaje es mayor a la que aguanta el vehículo, lanza la excepción
        if carga_kg > self._carga_maxima_kg:
            raise CargaExcedidaError(self._placa, carga_kg, self._carga_maxima_kg)

    def VerificarDocumentos(self, fecha):
        # le pasa la tarea a Documentacion, que es la que sabe si algo está vencido
        self._documentacion.VerificarVigencia(fecha, self._placa)

    def ShowInformation(self):
        # Las hijas lo sobrescriben y le agregan sus propios datos
        return (f"Placa: {self._placa} | Marca: {self._marca} | Modelo: {self._modelo}\n"
                f"Carga máxima: {self._carga_maxima_kg} kg | Licencia requerida: {self._categoria_licencia}\n"
                f"{self._documentacion.ShowInformation()}")

    @abstractmethod
    def CalcularCostoViaje(self, distancia_km):
        # Cada hija lo calcula a su manera, Vehiculo no sabe cuánto cobra cada tipo
        pass

    @abstractmethod
    def PerformMainActivity(self):
        # Cada hija define qué tipo de carga mueve; Vehiculo no lo implementa
        pass

    def __str__(self):
        return self.ShowInformation()


if __name__ == "__main__":
    # Prueba rápida: Vehiculo es abstracta, así que no se puede crear directamente
    try:
        v = Vehiculo("ABC123", "Chevrolet", 2020, 8000, "C2", date(2027, 3, 15), date(2027, 1, 10))
    except TypeError as error:
        print(f"No se puede crear un Vehiculo directamente: {error}")