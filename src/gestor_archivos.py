import os
from pathlib import Path
import json
import csv
import shutil
import logging
from typing import List
from src.configuracion import RUTA_DATOS, RUTA_TXT, RUTA_CSV, RUTA_JSON, RUTA_LOG

# Configurar logging para escribir en RUTA_LOG
def _config_logger():
    RUTA_DATOS.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("gestor_archivos")
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fh = logging.FileHandler(RUTA_LOG, encoding='utf-8')
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    return logger

_logger = _config_logger()

def registrar_log(mensaje: str):
    _logger.info(mensaje)

def crear_estructura():
    """
    Crea 'datos', 'datos/txt', 'datos/csv', 'datos/json' si no existen.
    """
    try:
        RUTA_DATOS.mkdir(parents=True, exist_ok=True)
        RUTA_TXT.mkdir(parents=True, exist_ok=True)
        RUTA_CSV.mkdir(parents=True, exist_ok=True)
        RUTA_JSON.mkdir(parents=True, exist_ok=True)
        registrar_log("Estructura de carpetas creada/verificada.")
    except Exception as e:
        registrar_log(f"Error creando estructura de carpetas: {e}")
        raise

def guardar_txt(registros: List[dict], nombre_archivo="registros.txt"):
    """
    Guarda registros en formato legible .txt (una línea por registro, JSON-like).
    """
    crear_estructura()
    ruta = RUTA_TXT / nombre_archivo
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            for reg in registros:
                f.write(json.dumps(reg, ensure_ascii=False) + "\n")
        registrar_log(f"Archivo TXT guardado: {ruta}")
        return ruta
    except Exception as e:
        registrar_log(f"Error guardando TXT: {e}")
        raise

def guardar_csv(registros: List[dict], nombre_archivo="registros.csv"):
    crear_estructura()
    ruta = RUTA_CSV / nombre_archivo
    if not registros:
        registrar_log("Guardar CSV: lista de registros vacía.")
        return ruta
    try:
        campos = list(registros[0].keys())
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=campos)
            writer.writeheader()
            for reg in registros:
                writer.writerow(reg)
        registrar_log(f"Archivo CSV guardado: {ruta}")
        return ruta
    except Exception as e:
        registrar_log(f"Error guardando CSV: {e}")
        raise

def guardar_json(registros: List[dict], nombre_archivo="registros.json"):
    crear_estructura()
    ruta = RUTA_JSON / nombre_archivo
    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(registros, f, indent=4, ensure_ascii=False)
        registrar_log(f"Archivo JSON guardado: {ruta}")
        return ruta
    except Exception as e:
        registrar_log(f"Error guardando JSON: {e}")
        raise

def importar_json(ruta_archivo: Path):
    """
    Importa un JSON desde 'ruta_archivo' y devuelve el contenido (lista/dict).
    """
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            contenido = json.load(f)
        registrar_log(f"Archivo JSON importado: {ruta_archivo}")
        return contenido
    except Exception as e:
        registrar_log(f"Error importando JSON {ruta_archivo}: {e}")
        raise

def mover_archivo(origen: Path, destino_carpeta: Path):
    """
    Mueve un archivo a una carpeta destino (crea la carpeta si hace falta).
    """
    try:
        destino_carpeta.mkdir(parents=True, exist_ok=True)
        destino = destino_carpeta / origen.name
        shutil.move(str(origen), str(destino))
        registrar_log(f"Archivo movido: {origen} -> {destino}")
        return destino
    except Exception as e:
        registrar_log(f"Error moviendo archivo {origen} a {destino_carpeta}: {e}")
        raise
