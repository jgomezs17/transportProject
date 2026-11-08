# transportProject: sistema de gestión de transporte de carga

Proyecto final en Python para el curso de Programación Orientada a Objetos de la Universidad de Manizales (Facultad de Ciencias e Ingenierías), correspondiente a la Actividad Colaborativa N°3.

**Integrantes:** Jonathan Gómez Salazar y Omar Picón Meza

---

## Problema que resuelve

Una empresa de transporte de carga necesita saber, antes de enviar un camión a la carretera, si ese viaje se puede realizar: si la carga cabe en el vehículo, si sus documentos están vigentes y si el conductor tiene la licencia que exige ese tipo de vehículo. Si alguna condición falla, el viaje no se programa.

El sistema registra la flota, los conductores y los viajes, calcula el costo de cada viaje según el tipo de vehículo y controla con excepciones las situaciones que impiden programarlo.

## Estructura del proyecto

```
transportProject/
├── main.py                        # Archivo principal: ejecuta todas las pruebas
├── README.md
├── docs/                          # Diagrama UML y Documento de Decisiones de Diseño
├── exceptions/
│   └── excepciones.py             # Las 3 excepciones personalizadas
└── models/
    ├── vehiculo.py                # Clase abstracta (padre)
    ├── camion_furgon.py
    ├── tractocamion.py
    ├── volqueta.py
    ├── conductor.py
    ├── documentacion.py
    └── viaje.py
```

## Clases principales

| Clase | Responsabilidad |
|---|---|
| `Vehiculo` (abstracta) | Datos comunes de cualquier vehículo: placa, marca, modelo, carga máxima, categoría de licencia que exige y su documentación. Define los métodos abstractos `CalcularCostoViaje()` y `PerformMainActivity()`. |
| `CamionFurgon` | Hereda de `Vehiculo`. Furgón cerrado para mercancía empacada; puede ser refrigerado. |
| `Tractocamion` | Hereda de `Vehiculo`. Cabezote que arrastra un remolque para carga pesada. |
| `Volqueta` | Hereda de `Vehiculo`. Platón basculante para material de construcción. |
| `Documentacion` | Fechas de vencimiento del SOAT y de la revisión técnico-mecánica, y verificación de vigencia. |
| `Conductor` | Datos del conductor y su licencia, y verificación de si está habilitado para un vehículo. |
| `Viaje` | Une un vehículo y un conductor con un origen, un destino, una distancia y una carga. Programa el viaje y calcula su costo. |

## Herencia: Vehiculo es una clase abstracta

`Vehiculo` hereda de `ABC` y declara `CalcularCostoViaje()` y `PerformMainActivity()` con `@abstractmethod`. Es abstracta porque en una empresa de carga no existe un "vehículo genérico": siempre es un camión furgón, un tractocamión o una volqueta. Un `Vehiculo` suelto no sabría cuánto cobrar por kilómetro ni qué tipo de carga mueve, así que no debe poder crearse. Si se intenta, Python lanza un `TypeError`, que `main.py` demuestra y captura.

La herencia representa una relación "es un": un camión furgón **es un** vehículo, un tractocamión **es un** vehículo y una volqueta **es un** vehículo. Cada hija llama a `super().__init__()` y no repite lo que ya está en `Vehiculo`.

**Común a las hijas (definido en `Vehiculo`):**
- Atributos: placa, marca, modelo, carga máxima en kg, categoría de licencia y documentación.
- Métodos: getters y setters validados, `ValidarCarga()`, `VerificarDocumentos()`, `ShowInformation()` y `__str__()`.

**Propio de cada hija:**

| Clase | Atributos propios | Cálculo del costo por kilómetro |
|---|---|---|
| `CamionFurgon` | volumen en m³, refrigerado | 3.000 pesos, con un recargo del 25% si es refrigerado |
| `Tractocamion` | número de ejes, tipo de remolque | 4.000 pesos más 800 por cada eje |
| `Volqueta` | tipo de material, capacidad en m³ | 3.500 pesos multiplicado por un factor según el material (arena 1,0; grava 1,1; escombros 1,2) |

Cada hija fija la categoría de licencia que exige su tipo de vehículo: C2 para el camión furgón y la volqueta, y C3 para el tractocamión. Las tarifas y las categorías son valores de ejemplo, una simplificación del sistema.

## Sobrescritura y polimorfismo

Las tres hijas sobrescriben `CalcularCostoViaje()`, `PerformMainActivity()` y `ShowInformation()`, con el mismo nombre pero un resultado distinto según sus datos propios (por ejemplo, 100 km cuestan 375.000 pesos en un furgón refrigerado, 800.000 en un tractocamión de cinco ejes y 420.000 en una volqueta de escombros).

En `main.py` hay una única lista `flota` con vehículos de los tres tipos, recorrida con un solo ciclo que llama a los mismos métodos sin preguntar por el tipo. Python decide en ejecución qué versión usar.

## Composición: Vehiculo y Documentacion

El constructor de `Vehiculo` crea su propio objeto `Documentacion` a partir de las fechas de vencimiento que recibe. Es composición porque los documentos pertenecen a un vehículo concreto, no se comparten y no tienen sentido sin él: si el vehículo deja de existir, su documentación también.

No se resolvió con herencia porque un vehículo **no es** una documentación; la relación correcta es "tiene un".

## Asociaciones

`Viaje` se asocia con un `Vehiculo` y con un `Conductor`. Estos existen antes y después del viaje y pueden participar en varios, por eso `Viaje` solo guarda la referencia. Los setters validan con `isinstance` que se reciban objetos del tipo correcto.

## Excepciones personalizadas

Todas heredan de `Exception`, están en `exceptions/excepciones.py` y se capturan con `try/except` en `main.py`, de modo que el programa continúa después de cada error.

| Excepción | Situación que controla | Dónde se lanza |
|---|---|---|
| `CargaExcedidaError` | La carga del viaje supera lo que soporta el vehículo | `Vehiculo.ValidarCarga()` |
| `ConductorNoHabilitadoError` | Licencia vencida o categoría insuficiente para el vehículo | `Conductor.VerificarHabilitacion()` |
| `DocumentosVencidosError` | SOAT o revisión técnico-mecánica vencidos | `Documentacion.VerificarVigencia()` |

`Viaje.Programar(fecha)` llama a las tres verificaciones en orden (carga, documentos y licencia). Si alguna lanza su excepción, el viaje queda en estado `pendiente`; solo si las tres pasan cambia a `programado`.

Las validaciones de los setters (por ejemplo, una distancia negativa) siguen informando el error sin aplicar el cambio.

## Cómo ejecutar

Requisitos: Python 3.

Desde la carpeta del proyecto:

```
py main.py
```

(o `python main.py`, según el sistema). El archivo `main.py` crea más de ocho objetos y muestra, en este orden: la clase abstracta que no se puede instanciar, las validaciones, la composición, el recorrido polimórfico de la flota, los viajes programados y los cuatro casos de excepción (carga excedida, licencia insuficiente, licencia vencida y SOAT vencido).

Cada clase de `models/` también se puede probar por separado, por ejemplo:

```
py -m models.vehiculo
py -m models.viaje
```

## Documentación

En la carpeta `docs/` están el diagrama UML de clases y el Documento de Decisiones de Diseño.

## Uso de herramientas de inteligencia artificial

Se utilizó Claude (Anthropic) como apoyo para comprender cómo aplicar los conceptos a un contexto nuevo, proponer el diseño de las clases, generar fragmentos de código que luego se adaptaron al estilo del proyecto y revisar errores. El código se probó clase por clase y con `main.py`. El detalle de este uso, incluidas las propuestas que se modificaron o descartaron, se declara en el Documento de Decisiones de Diseño.
