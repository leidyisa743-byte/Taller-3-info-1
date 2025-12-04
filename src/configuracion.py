from pathlib import Path

# Ruta raíz del proyecto (dos niveles arriba si se importa desde src)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Rutas de datos
RUTA_DATOS = PROJECT_ROOT / "datos"
RUTA_TXT = RUTA_DATOS / "txt"
RUTA_CSV = RUTA_DATOS / "csv"
RUTA_JSON = RUTA_DATOS / "json"
RUTA_LOG = RUTA_DATOS / "log.txt"

# MongoDB (rellena MONGO_URI con tu cadena de conexión de Atlas si la tienes)
MONGO_URI = "mongodb+srv://leidyisa743_db_user:2U8OJGpMv7RNNHrd@cluster0.ykqyrie.mongodb.net/?appName=Cluster0"  # e.g. "mongodb+srv://usuario:clave@cluster0.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "taller_info1"
COLLECTION_NAME = "signos_vitales"
