import sys
from pathlib import Path
import json

# Asegurar que el paquete src se pueda importar
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.generador import generar_datos_aleatorios, ordenar_por_fc
from src.validaciones import validar_registros, validar_patrones
from src.gestor_archivos import (
    crear_estructura, guardar_txt, guardar_csv, guardar_json,
    importar_json, registrar_log
)
from src.base_datos import insertar_datos_mongo, ejecutar_consultas_y_exportar
from src.configuracion import RUTA_JSON

def imprimir_menu():
    print("""
Taller 3 - Gestión de Información
1) Generar datos aleatorios (50)
2) Validar y ordenar datos generados
3) Guardar datos en TXT, CSV y JSON
4) Importar datos desde JSON
5) Conectar a MongoDB e insertar datos validados
6) Ejecutar consultas MongoDB (promedio FC, SpO2<94) y exportar resultados
7) Mostrar un registro de ejemplo y validación detallada
0) Salir
""")

def main():
    crear_estructura()
    registros_actuales = []

    while True:
        imprimir_menu()
        opt = input("Elige opción: ").strip()
        if opt == "1":
            n = input("¿Cuántos registros quieres generar? [default 50]: ").strip() or "50"
            try:
                n = int(n)
            except:
                print("Número inválido. Usando 50.")
                n = 50
            registros_actuales = generar_datos_aleatorios(n)
            print(f"Generados {len(registros_actuales)} registros.")
            registrar_log(f"Generados {len(registros_actuales)} registros aleatorios.")
        elif opt == "2":
            if not registros_actuales:
                print("No hay registros en memoria. Genera o importa primero.")
                continue
            validos, invalidos = validar_registros(registros_actuales)
            print(f"Válidos: {len(validos)} | Inválidos: {len(invalidos)}")
            if invalidos:
                print("Algunos registros no cumplen el patrón. Se muestran abajo:")
                for reg, errs in invalidos[:10]:
                    print(reg, "-> errores en:", errs)
            registros_actuales = ordenar_por_fc(validos)
            registrar_log(f"Validación realizada. Válidos: {len(validos)}. Ordenados por FC.")
        elif opt == "3":
            if not registros_actuales:
                print("No hay registros en memoria. Genera o importa primero.")
                continue
            nombre_base = input("Nombre base archivo (sin extensión) [registros]: ").strip() or "registros"
            guardar_txt(registros_actuales, nombre_archivo=f"{nombre_base}.txt")
            guardar_csv(registros_actuales, nombre_archivo=f"{nombre_base}.csv")
            guardar_json(registros_actuales, nombre_archivo=f"{nombre_base}.json")
            print("Archivos guardados en datos/txt, datos/csv, datos/json.")
        elif opt == "4":
            ruta = input("Ruta al JSON a importar (ej: datos/json/registros.json): ").strip() or str(RUTA_JSON / "registros.json")
            ruta_path = Path(ruta)
            if not ruta_path.exists():
                print("Archivo no encontrado:", ruta_path)
                continue
            contenido = importar_json(ruta_path)
            if isinstance(contenido, list):
                registros_actuales = contenido
                print(f"Importados {len(contenido)} registros.")
                registrar_log(f"Importados {len(contenido)} registros desde {ruta_path}")
            else:
                print("Contenido JSON no es lista de registros.")
        elif opt == "5":
            if not registros_actuales:
                print("No hay registros en memoria. Genera o importa primero.")
                continue
            # Validar antes de insertar
            validos, invalidos = validar_registros(registros_actuales)
            if invalidos:
                print(f"Existen {len(invalidos)} registros inválidos. No se insertará a Mongo until se corrijan.")
                registrar_log("Intento de inserción a Mongo con registros inválidos. Abortado.")
                continue
            # Insertar
            ok = insertar_datos_mongo(validos)
            if ok:
                registrar_log("Inserción a Mongo completada desde CLI.")
        elif opt == "6":
            ejecutar_consultas_y_exportar()
        elif opt == "7":
            # Mostrar ejemplo y validación detallada
            if not registros_actuales:
                print("No hay registros en memoria. Genera o importa primero.")
                continue
            ejemplo = registros_actuales[0]
            print("Registro ejemplo:", ejemplo)
            ok, errores = validar_patrones(ejemplo)
            print("Validación:", "Válido" if ok else f"Inválido - errores en {errores}")
        elif opt == "0":
            print("Saliendo. ¡Éxitos con el taller!")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    main()
