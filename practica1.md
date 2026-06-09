# 1. MARCO FORMATIVO

## 1.1. Valor

| Nombre del valor | ¿Cómo se aplica en tu laboratorio? |
|---|---|
| Perseverancia | El estudiante analiza distintas alternativas para encontrar la mejor ruta, corrigiendo errores y mejorando su solución hasta obtener resultados correctos. |

## 1.2. Competencia(s)

Con la elaboración de esta práctica el estudiante adquirirá la siguiente competencia:

**Desarrollar soluciones basadas en programación lógica utilizando Prolog para representar conocimiento, realizar búsquedas en grafos y resolver problemas de optimización mediante reglas y relaciones lógicas.**

## 1.3. Habilidad(es) blandas a formar

La práctica le permitirá desarrollar las siguientes habilidades:

- Pensamiento lógico y analítico.
- Resolución de problemas.
- Atención al detalle.
- Capacidad de investigación.
- Organización y estructuración de conocimiento.

---

# 2. Resultado del Aprendizaje

## 2.1. Objetivo SMART

| Específico (¿Qué?) | Medible (¿Cuánto?) | Alcanzable (¿Cómo?) | Realista (¿Para qué?) | A Tiempo (¿Cuándo?) |
|---|---|---|---|---|
| Desarrollar un sistema en Prolog capaz de encontrar la ruta más corta entre dos ciudades. | El programa deberá gestionar al menos 8 ciudades y encontrar correctamente la ruta óptima en las pruebas realizadas. | Implementando hechos, reglas, listas y algoritmos de búsqueda en Prolog. | Para fortalecer las competencias en programación lógica y representación de conocimiento. | Al finalizar la práctica y entregar el proyecto en la fecha establecida. |

---

# 3. Enunciado de la Práctica

## 3.1 Descripción del problema a resolver

Una empresa de transporte interdepartamental desea contar con un sistema capaz de determinar la ruta más corta entre distintas ciudades conectadas por carreteras. Actualmente, las rutas y distancias se conocen, pero no existe un mecanismo automatizado que permita identificar el recorrido óptimo entre un punto de origen y un destino.

Para resolver este problema, se desarrollará una solución híbrida donde **Prolog será el encargado de representar el conocimiento y realizar la inferencia lógica para encontrar rutas y calcular distancias**, mientras que **Python actuará como backend**, permitiendo recibir solicitudes del usuario, ejecutar consultas en Prolog y mostrar los resultados obtenidos.

El sistema deberá permitir seleccionar una ciudad de origen y una ciudad destino, obteniendo como resultado la ruta recomendada y la distancia total recorrida.

## 3.2 Alcance de la práctica

La práctica debe cumplir con las siguientes funcionalidades mínimas:

- Definir una **base de conocimiento en Prolog** con al menos **10 ciudades** y sus respectivas conexiones.
- Representar las distancias entre ciudades mediante hechos, indicando el origen, destino y distancia.
- Permitir la búsqueda de rutas entre dos ciudades ingresadas por el usuario.
- Evitar ciclos o rutas repetitivas, es decir, que una misma ciudad no se repita dentro de una ruta.
- Calcular la distancia total de cada ruta encontrada.
- Determinar automáticamente la **ruta más corta** entre una ciudad de origen y una ciudad destino.
- Implementar un **backend en Python** que permite ejecutar consultas hacia Prolog.
- Utilizar Prolog como motor principal de la lógica; Python solo debe encargarse de enviar consultas y mostrar resultados.
- Mostrar al usuario la ruta encontrada y la distancia total recorrida.
- Desarrollar un **frontend funcional e intuitivo**, donde el usuario pueda seleccionar o ingresar ciudades.
- Permitir agregar nuevas ciudades y conexiones desde el frontend. Los nuevos datos se gestionan en memoria durante la sesión; al confirmar los cambios, Python generará un nuevo archivo `.pl` con los hechos actualizados, sin modificar el archivo Prolog original. El archivo original actúa como base de conocimiento inicial de solo lectura.
- Mostrar todas las rutas posibles entre dos ciudades, junto con su distancia total.
- Implementar algún patrón de arquitectura para el backend.
- Manual de usuario donde se explique claramente cómo usar el sistema (en formato `.md`).
- Manual técnico donde se explique claramente el patrón de arquitectura y mejoras al sistema (en formato `.md`).

### Funcionalidades recomendadas

- Comparar varias rutas y presentar estadísticas.
- Validar que las ciudades ingresadas existan en la base de conocimiento.
- Mostrar mensajes claros cuando no exista una ruta disponible.
- Manejo de errores.
- Ordenar las rutas de menor a mayor distancia.
- Permitir reiniciar o limpiar la búsqueda desde la interfaz.
- Presentar la información de forma visual, por ejemplo mediante tarjetas, tablas o listas.

### Restricciones

- La lógica de búsqueda y optimización deberá implementarse exclusivamente en Prolog.
- Python únicamente actuará como capa de integración y ejecución de consultas.
- No se permite implementar el algoritmo de búsqueda de rutas directamente en Python.
- No se puede usar bases de datos.
- El archivo Prolog original (`.pl`) no debe ser modificado directamente. Para persistir nuevas ciudades o conexiones, Python deberá generar un nuevo archivo `.pl` derivado que extienda la base de conocimiento original.

## 3.3 Requerimientos técnicos

Para el desarrollo de esta práctica se deberán utilizar las siguientes tecnologías:

### Lenguajes y herramientas

- Prolog (SWI-Prolog) para la representación del conocimiento y la lógica de inferencia.
- Python 3.x para el desarrollo del backend.
- Librería PySwip o mecanismo equivalente para la comunicación entre Python y Prolog.

### Requisitos mínimos del sistema

- Base de conocimiento con al menos 10 ciudades.
- Archivo Prolog (`.pl`) con los hechos y reglas necesarias.
- Aplicación Python capaz de ejecutar consultas hacia Prolog.
- Evidencia de ejecución mediante capturas de pantalla o consola.
- Mecanismo de generación de nuevo archivo `.pl` desde Python cuando se agreguen ciudades o conexiones desde el frontend.

---

# 4. Entregables

| Tipo | Descripción |
|---|---|
| Código fuente Prolog | Archivo `.pl` que contenga la base de conocimiento, reglas de búsqueda de rutas, cálculo de distancias y determinación de la ruta más corta. |
| Backend | Proyecto desarrollado en Python encargado de la comunicación entre el frontend y Prolog. Debe implementar el patrón de arquitectura seleccionado. |
| Frontend | Interfaz gráfica funcional que permita consultar rutas, visualizar resultados y administrar ciudades y conexiones. |
| Manual de Usuario | Documento en formato `.md` que explique la instalación, ejecución y uso del sistema mediante ejemplos e imágenes. |
| Manual Técnico | Documento en formato `.md` que describa la arquitectura implementada, estructura del proyecto, integración Python-Prolog y posibles mejoras futuras. |
| Evidencias de Ejecución | Capturas de pantalla o registros de ejecución que demuestren el funcionamiento de las funcionalidades solicitadas. |
| Repositorio del Proyecto | Enlace al repositorio Git que contenga el código fuente, documentación y control de versiones del proyecto. |

---

# 5. Material de apoyo

Se recomienda consultar los siguientes recursos para comprender la integración entre Python y Prolog, así como los conceptos de programación lógica y búsqueda de rutas.

- Documentación oficial de SWI-Prolog: https://www.swi-prolog.org
- Tutorial de Prolog para principiantes: https://www.learnprolognow.org
- Documentación de PySwip: https://pyswip.readthedocs.io
- Tutorial de FastAPI: https://fastapi.tiangolo.com
- Repositorio oficial de Git: https://git-scm.com/doc

---

# 6. Recursos y herramientas a utilizar

## Software / Hardware

- Computadora personal con sistema operativo Windows, Linux o macOS.
- Python 3.11 o superior.
- SWI-Prolog.
- Visual Studio Code u otro entorno de desarrollo integrado (IDE).
- Git para control de versiones.
- Navegador web actualizado.

## Plataformas

- GitHub para alojamiento del repositorio y control de versiones.
- UEDI para la entrega de la práctica.

## Nombre obligatorio del repositorio

El repositorio deberá nombrarse utilizando el siguiente formato:

```
[IA1]_VACASJUN2026_{NOMBRE}_{CARNET}
```

**FECHA DE ENTREGA: 06/06/2025**
