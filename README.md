Taller 3 – Gestión de Información y Bases de Datos
Informática II – Universidad de Antioquia
Integrantes:
    - Isabela Arrieta Pacheco
    - Leidy Zapata Hoyos

Descripción general
Este proyecto implementa un sistema completo para la generación, validación, almacenamiento y consulta de registros biomédicos utilizando Python. Incluye manejo de archivos TXT/CSV/JSON, validación mediante expresiones regulares, organización automática de directorios, registro de acciones en un log y conexión con MongoDB Atlas para almacenar y consultar datos en una colección NoSQL.

El sistema sigue las buenas prácticas solicitadas en el taller: modularidad, manejo de excepciones, reproducibilidad y uso adecuado de GitHub.

1. Generación y ordenamiento de datos
- Se generan al menos 50 registros biomédicos aleatorios, cada uno con:
  id: formato "ID-001"
  fr: edad ("18 Años")
  fc: frecuencia cardiaca ("090ppm")
  spo2: saturación de oxígeno ("95%")
- Los datos se ordenan por frecuencia cardiaca ascendente.

2. Gestión de archivos: TXT, CSV y JSON
- Exportación de los registros ordenados en formatos .txt, .csv y .json.
- Importación desde archivos JSON.
- Manejo de rutas, verificación de directorios y manejo de excepciones.

3. Herramientas del sistema
- Creación automática de la estructura de carpetas:
  /data/txt
  /data/csv
  /data/json
- Organización automática de los archivos generados.
- Registro de todas las acciones en log.txt utilizando la librería logging.

4. Validación con expresiones regulares
Cada campo se valida mediante expresiones regulares que aseguran que su formato sea correcto:
  id: ^ID-\d{3}$
  fr: ^\d{2} Años$
  fc: ^\d{3}ppm$
  spo2: ^\d{2}%$
Solo los registros válidos se exportan e insertan en MongoDB.

5. MongoDB (NoSQL)
- Conexión a MongoDB Atlas.
- Creación y uso de la colección "signos_vitales".
- Inserción de los registros validados.
- Consultas requeridas:
  - Promedio de frecuencia cardiaca.
  - Documentos con SpO2 menor a 94.
- Exportación de los resultados a resultados_mongo.json.

6. Integración final (main.py)
El archivo principal ofrece un menú interactivo para:
- Generar datos.
- Validar y ordenar registros.
- Importar y exportar archivos.
- Conectarse a MongoDB.
- Ejecutar consultas y mostrar resultados.
- Mostrar un registro con validación detallada.

El sistema está automatizado y diseñado para ejecutarse desde cualquier entorno con Python 3.

7. GitHub
- Repositorio privado que incluye:
  - Código fuente organizado por módulos.
  - Archivo README.
  - Al menos cinco commits con mensajes adecuados.

Ejecución
python main.py