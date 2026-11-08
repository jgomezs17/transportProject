from datetime import date
from models.vehiculo import Vehiculo
from models.camion_furgon import CamionFurgon
from models.tractocamion import Tractocamion
from models.volqueta import Volqueta
from models.conductor import Conductor
from models.viaje import Viaje
from exceptions.excepciones import (CargaExcedidaError,
                                    ConductorNoHabilitadoError,
                                    DocumentosVencidosError)

# fecha en la que se programan los viajes
fecha_viaje = date(2026, 11, 8)

## ===== Fase 1: Vehiculo es abstracta =====
print("===== Vehiculo abstracta =====")
# No se debe poder crear un Vehiculo directamente
try:
    vehiculo1 = Vehiculo("ABC123", "Chevrolet", 2020, 8000, "C2", date(2027, 3, 15), date(2027, 1, 10))
except TypeError as error:
    print(f"No se puede crear un Vehiculo directamente: {error}")
print("El programa sigue funcionando despues del error.")

## ===== Fase 2: creacion de vehiculos =====
print("\n===== Creacion de vehiculos =====")
furgon1 = CamionFurgon("FUR123", "Hino", 2021, 6000, date(2027, 4, 1), date(2027, 2, 15), 30, True)
furgon2 = CamionFurgon("FUR456", "Chevrolet", 2020, 4500, date(2027, 3, 10), date(2027, 6, 20), 22, False)
tracto1 = Tractocamion("TRA123", "Kenworth", 2019, 30000, date(2027, 5, 10), date(2027, 3, 20), 5, "cisterna")
tracto2 = Tractocamion("TRA456", "Volvo", 2022, 34000, date(2027, 8, 1), date(2027, 9, 15), 6, "plataforma")
volqueta1 = Volqueta("VOL123", "Chevrolet", 2018, 12000, date(2027, 1, 30), date(2027, 2, 28), "escombros", 14)
volqueta2 = Volqueta("VOL456", "Dodge", 2017, 10000, date(2027, 2, 20), date(2027, 4, 5), "arena", 12)
print("Se crearon 2 camiones furgon, 2 tractocamiones y 2 volquetas.")

print("\n===== Validaciones de vehiculos =====")
# Valores invalidos: deben informar el error y NO cambiar el dato
furgon1.SetPlaca("   ")
furgon1.SetModelo(1900)
furgon1.SetCargaMaximaKg(-500)
furgon1.SetVolumenM3(0)
furgon1.SetRefrigerado("si")
tracto1.SetNumeroEjes(1)
tracto1.SetTipoRemolque("jaula")
volqueta1.SetTipoMaterial("madera")
volqueta1.SetCapacidadM3(-3)
print(furgon1.ShowInformation())    # tiene que seguir igual

# Vehiculo creado con datos invalidos: avisa y deja esos campos vacios
vehiculo_malo = CamionFurgon("", "Hino", 1900, -1, date(2027, 1, 1), date(2027, 1, 1), 0, "si")

## ===== Fase 3: conductores =====
print("\n===== Conductores =====")
conductor1 = Conductor("Luis Ortiz", "1010", "LIC-001", "C2", date(2028, 5, 20))
conductor2 = Conductor("Ana Rios", "2020", "LIC-002", "C3", date(2029, 1, 1))
conductor3 = Conductor("Pedro Gil", "3030", "LIC-003", "C3", date(2026, 1, 1))   # licencia ya vencida
print(conductor1.ShowInformation())
print(conductor2.ShowInformation())

print("\n===== Validaciones de Conductor =====")
conductor1.SetNombre("   ")
conductor1.SetCategoriaLicencia("B1")
conductor1.SetVencimientoLicencia("2028-05-20")    # un texto no es una fecha
print(conductor1.ShowInformation())                # tiene que seguir igual

## ===== Fase 4: composicion Vehiculo - Documentacion =====
print("\n===== Composicion: cada vehiculo tiene su Documentacion =====")
print(f"Documentos de {furgon1.GetPlaca()}: {furgon1.GetDocumentacion().ShowInformation()}")
print(f"Documentos de {tracto1.GetPlaca()}: {tracto1.GetDocumentacion().ShowInformation()}")

## ===== Fase 5: recorrido polimorfico =====
# Una sola coleccion con los tres tipos de vehiculo
flota = [furgon1, furgon2, tracto1, tracto2, volqueta1, volqueta2]

print("\n===== Reporte general de la flota =====")
for vehiculo in flota:
    print(vehiculo.ShowInformation())
    print(vehiculo.PerformMainActivity())
    print(f"Costo de un viaje de 100 km: ${vehiculo.CalcularCostoViaje(100):,.0f}")
    print("-" * 40)

## ===== Fase 6: viajes programados =====
print("\n===== Viajes programados =====")
viaje1 = Viaje("V001", "Bogota", "Medellin", 415, 25000, tracto1, conductor2)
viaje2 = Viaje("V002", "Bogota", "Tunja", 150, 4000, furgon1, conductor1)
viaje3 = Viaje("V003", "Bogota", "Villavicencio", 90, 9000, volqueta1, conductor1)

viaje1.Programar(fecha_viaje)
viaje2.Programar(fecha_viaje)
viaje3.Programar(fecha_viaje)

print()
print(viaje1.ShowInformation())
print(viaje2.ShowInformation())
print(viaje3.ShowInformation())

print("\n===== Validaciones de Viaje =====")
viaje1.SetDistanciaKm(-20)
viaje1.SetCargaKg(0)
viaje1.SetVehiculo("TRA123")          # un texto no es un Vehiculo
viaje1.SetConductor("Ana Rios")       # un texto no es un Conductor
viaje1.Programar("2026-11-08")        # un texto no es una fecha

## ===== Fase 7: excepciones personalizadas =====
print("\n===== Excepciones: viajes que no se pueden programar =====")

# 1. La carga es mayor a la que aguanta el vehiculo
viaje4 = Viaje("V004", "Bogota", "Cali", 460, 35000, tracto1, conductor2)
try:
    viaje4.Programar(fecha_viaje)
except (CargaExcedidaError, ConductorNoHabilitadoError, DocumentosVencidosError) as error:
    print(f"Error: {error}")
print(f"Estado del viaje V004: {viaje4.GetEstado()}")

# 2. El conductor tiene licencia C2 y el tractocamion pide C3
viaje5 = Viaje("V005", "Bogota", "Cali", 460, 20000, tracto2, conductor1)
try:
    viaje5.Programar(fecha_viaje)
except (CargaExcedidaError, ConductorNoHabilitadoError, DocumentosVencidosError) as error:
    print(f"Error: {error}")
print(f"Estado del viaje V005: {viaje5.GetEstado()}")

# 3. La licencia del conductor ya esta vencida
viaje6 = Viaje("V006", "Bogota", "Cali", 460, 20000, tracto2, conductor3)
try:
    viaje6.Programar(fecha_viaje)
except (CargaExcedidaError, ConductorNoHabilitadoError, DocumentosVencidosError) as error:
    print(f"Error: {error}")
print(f"Estado del viaje V006: {viaje6.GetEstado()}")

# 4. El SOAT del vehiculo ya esta vencido
furgon_vencido = CamionFurgon("VEN999", "Hino", 2015, 5000, date(2026, 9, 30), date(2027, 2, 15), 20, False)
viaje7 = Viaje("V007", "Bogota", "Tunja", 150, 3000, furgon_vencido, conductor1)
try:
    viaje7.Programar(fecha_viaje)
except (CargaExcedidaError, ConductorNoHabilitadoError, DocumentosVencidosError) as error:
    print(f"Error: {error}")
print(f"Estado del viaje V007: {viaje7.GetEstado()}")

print("\nEl programa continuo su ejecucion despues de controlar todas las excepciones.")