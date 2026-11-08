# Clase Conductor
# Persona que maneja los vehículos de la empresa, con su licencia de conducción.

from datetime import date
from exceptions.excepciones import ConductorNoHabilitadoError


class Conductor:
    # categorías de licencia que acepto, de menor a mayor
    CATEGORIAS = ["C1", "C2", "C3"]

    def __init__(self, nombre, cedula, numero_licencia, categoria_licencia, vencimiento_licencia):
        # valores vacíos por defecto: si el dato es inválido avisa y queda vacío
        self.__nombre = ""
        self.__cedula = ""
        self.__numero_licencia = ""
        self.__categoria_licencia = ""
        self.__vencimiento_licencia = None

        # uso los setters para que pasen por las validaciones
        self.SetNombre(nombre)
        self.SetCedula(cedula)
        self.SetNumeroLicencia(numero_licencia)
        self.SetCategoriaLicencia(categoria_licencia)
        self.SetVencimientoLicencia(vencimiento_licencia)

    # ---------- Getters ----------
    def GetNombre(self):
        return self.__nombre

    def GetCedula(self):
        return self.__cedula

    def GetNumeroLicencia(self):
        return self.__numero_licencia

    def GetCategoriaLicencia(self):
        return self.__categoria_licencia

    def GetVencimientoLicencia(self):
        return self.__vencimiento_licencia

    # ---------- Setters con validaciones ----------
    def SetNombre(self, nombre):
        if nombre is None or str(nombre).strip() == "":
            print("Error: el nombre del conductor no puede estar vacío. No se aplicó el cambio.")
            return
        self.__nombre = str(nombre).strip()

    def SetCedula(self, cedula):
        if cedula is None or str(cedula).strip() == "":
            print("Error: la cédula no puede estar vacía. No se aplicó el cambio.")
            return
        self.__cedula = str(cedula).strip()

    def SetNumeroLicencia(self, numero_licencia):
        if numero_licencia is None or str(numero_licencia).strip() == "":
            print("Error: el número de licencia no puede estar vacío. No se aplicó el cambio.")
            return
        self.__numero_licencia = str(numero_licencia).strip()

    def SetCategoriaLicencia(self, categoria_licencia):
        if categoria_licencia is None or str(categoria_licencia).strip().upper() not in Conductor.CATEGORIAS:
            print(f"Error: la categoría debe ser una de {Conductor.CATEGORIAS}. No se aplicó el cambio.")
            return
        self.__categoria_licencia = str(categoria_licencia).strip().upper()

    def SetVencimientoLicencia(self, vencimiento_licencia):
        # tiene que ser una fecha (date), no un texto suelto
        if not isinstance(vencimiento_licencia, date):
            print("Error: el vencimiento de la licencia debe ser una fecha. No se aplicó el cambio.")
            return
        self.__vencimiento_licencia = vencimiento_licencia

    # ---------- Métodos de la clase ----------
    def VerificarHabilitacion(self, categoria_requerida, fecha):
        # primero revisa que la licencia no esté vencida
        if self.__vencimiento_licencia is None or self.__vencimiento_licencia < fecha:
            raise ConductorNoHabilitadoError(self.__nombre, "la licencia está vencida")
        # la categoría del conductor tiene que ser igual o mayor a la que pide el vehículo
        if (self.__categoria_licencia not in Conductor.CATEGORIAS
                or categoria_requerida not in Conductor.CATEGORIAS):
            raise ConductorNoHabilitadoError(self.__nombre, "la categoría de la licencia no es válida")
        if Conductor.CATEGORIAS.index(self.__categoria_licencia) < Conductor.CATEGORIAS.index(categoria_requerida):
            raise ConductorNoHabilitadoError(
                self.__nombre,
                f"su licencia {self.__categoria_licencia} no alcanza para la categoría {categoria_requerida}")

    def ShowInformation(self):
        vence = str(self.__vencimiento_licencia) if self.__vencimiento_licencia is not None else "sin registrar"
        return (f"Conductor: {self.__nombre}\n"
                f"Cédula: {self.__cedula}\n"
                f"Licencia: {self.__numero_licencia} | Categoría: {self.__categoria_licencia} | Vence: {vence}")


if __name__ == "__main__":
    # Prueba rápida de la clase
    c = Conductor("Luis Ortiz", "1010", "LIC-001", "C2", date(2028, 5, 20))
    print(c.ShowInformation())

    # Habilitado: C2 alcanza para un vehículo que pide C2
    c.VerificarHabilitacion("C2", date(2026, 11, 8))
    print("Conductor habilitado")

    # No habilitado: C2 no alcanza para C3
    try:
        c.VerificarHabilitacion("C3", date(2026, 11, 8))
    except ConductorNoHabilitadoError as error:
        print(f"Error: {error}")

    # Datos inválidos: se informa y no se cambian
    c.SetCategoriaLicencia("B1")
    c.SetNombre("   ")