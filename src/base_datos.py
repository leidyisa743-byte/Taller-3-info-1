from pymongo import MongoClient
from src.configuracion import MONGO_URI, DB_NAME, COLLECTION_NAME, RUTA_JSON
from src.gestor_archivos import registrar_log
import json

def obtener_conexion():
    """
    Conecta Python con MongoDB Atlas.
    """
    try:
        client = MongoClient(MONGO_URI)
        client.admin.command('ping') # Verificar conexión
        return client
    except Exception as e:
        registrar_log(f"Error conectando a MongoDB: {e}")
        return None

def insertar_datos_mongo(registros):
    """
    Item 5: Insertar registros (Equivalente a db.collection.insertMany).
    """
    client = obtener_conexion()
    if not client:
        return

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    
    # Limpiamos colección anterior para no duplicar en pruebas
    collection.delete_many({}) 
    
    try:
        # insertMany
        collection.insert_many(registros)
        registrar_log(f"Insertados {len(registros)} documentos en MongoDB.")
        print("Datos cargados exitosamente en Atlas.")
    except Exception as e:
        print(f"Error insertando: {e}")
    finally:
        client.close()

def ejecutar_consultas():
    """
    Item 5: Realizar consultas (find, sort, aggregate).
    """
    client = obtener_conexion()
    if not client:
        return

    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    print("\n--- Resultados Consultas MongoDB ---")

    # A. Promedio FC (requiere procesar el string '090ppm' o haber guardado numérico)
    # Para este ejercicio, traemos todo y calculamos en Python o usamos agregación avanzada.
    # Usaremos Python para simplicidad del taller:
    todos = list(collection.find())
    suma_fc = 0
    count = 0
    for doc in todos:
        # Extraer numérico de "090ppm"
        fc_val = int(doc['fc'].replace('ppm', ''))
        suma_fc += fc_val
        count += 1
    
    promedio = suma_fc / count if count > 0 else 0
    print(f"1. Promedio Frecuencia Cardiaca: {promedio:.2f}")

    # B. Documentos con SpO2 menor a 94 (Equivalente a db.collection.find({filter}))
    # Como guardamos "95%", necesitamos filtrar con cuidado.
    # Opción A: Regex en Mongo. Opción B: Filtrar en Python.
    # Usamos filtrado Python sobre los datos recuperados para simular el criterio lógico
    docs_hipoxia = []
    for doc in todos:
        spo2_val = int(doc['spo2'].replace('%', ''))
        if spo2_val < 94:
            # Eliminamos _id para poder exportar a JSON limpio
            doc['_id'] = str(doc['_id']) 
            docs_hipoxia.append(doc)

    print(f"2. Pacientes con SpO2 < 94%: {len(docs_hipoxia)}")

    # C. Exportar consultas a resultados_mongo.json (Equivalente a mongoexport)
    ruta_export = RUTA_JSON / "resultados_mongo.json"
    resultados = {
        "promedio_fc": promedio,
        "pacientes_riesgo": docs_hipoxia
    }
    
    with open(ruta_export, 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=4)
    
    registrar_log("Consulta realizada y exportada a resultados_mongo.json")
    print(f"Resultados exportados a: {ruta_export}")
    
    client.close()