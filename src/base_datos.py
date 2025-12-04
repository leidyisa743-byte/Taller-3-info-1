import json
from src.configuracion import MONGO_URI, DB_NAME, COLLECTION_NAME, RUTA_JSON
from src.gestor_archivos import registrar_log
from pymongo import MongoClient
from pathlib import Path

def obtener_conexion():
    """
    Intenta conectar a MongoDB si MONGO_URI está configurado.
    Retorna MongoClient o None.
    """
    if not MONGO_URI:
        registrar_log("MONGO_URI no configurado. Omitiendo conexión a MongoDB.")
        return None
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        registrar_log("Conexión a MongoDB exitosa.")
        return client
    except Exception as e:
        registrar_log(f"Error conectando a MongoDB: {e}")
        return None

def insertar_datos_mongo(registros):
    client = obtener_conexion()
    if not client:
        print("No hay conexión a MongoDB (MONGO_URI vacío o error).")
        return False
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
    
        # Insertar
        # Convertir si los documentos tienen tipos no serializables (no es el caso aquí)
        collection.insert_many(registros)
        registrar_log(f"Insertados {len(registros)} documentos en MongoDB.")
        print(f"Insertados {len(registros)} documentos en MongoDB.")
        return True
    except Exception as e:
        registrar_log(f"Error insertando en MongoDB: {e}")
        print(f"Error insertando en MongoDB: {e}")
        return False
    finally:
        client.close()

def ejecutar_consultas_y_exportar():
    """
    Realiza:
    - Promedio de FC
    - Documentos con SpO2 < 94
    - Exporta resultados a resultados_mongo.json dentro de datos/json
    """
    client = obtener_conexion()
    if not client:
        print("No hay conexión a MongoDB (MONGO_URI vacío o error).")
        return None
    try:
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        todos = list(collection.find())
        if not todos:
            print("Colección vacía.")
            return None

        # Promedio FC
        suma = 0
        cnt = 0
        riesgos = []
        for doc in todos:
            fc_val = int(str(doc.get('fc', '0')).replace('ppm', ''))
            suma += fc_val
            cnt += 1
            spo2_val = int(str(doc.get('spo2', '0')).replace('%', ''))
            if spo2_val < 94:
                # convertir _id a str para exportar
                doc_copy = doc.copy()
                doc_copy['_id'] = str(doc_copy.get('_id'))
                riesgos.append(doc_copy)
        promedio = (suma / cnt) if cnt else 0

        resultados = {
            "promedio_fc": promedio,
            "pacientes_riesgo": riesgos
        }

        ruta_export = RUTA_JSON / "resultados_mongo.json"
        ruta_export.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta_export, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, indent=4, ensure_ascii=False)

        registrar_log("Consultas ejecutadas y exportadas a resultados_mongo.json")
        print(f"Promedio FC: {promedio:.2f}")
        print(f"Pacientes con SpO2 < 94%: {len(riesgos)}")
        print(f"Resultados exportados a {ruta_export}")
        return resultados
    except Exception as e:
        registrar_log(f"Error ejecutando consultas en MongoDB: {e}")
        print(f"Error ejecutando consultas: {e}")
        return None
    finally:
        client.close()