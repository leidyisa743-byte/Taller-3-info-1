import random

def generar_datos_aleatorios(cantidad):
    """
    Genera 'cantidad' registros biomédicos con formatos:
    - id: ID-001
    - fr: '18 Años'
    - fc: '090ppm'
    - spo2: '95%'
    """
    registros = []
    for i in range(1, cantidad + 1):
        id_str = f"ID-{i:03d}"
        edad = random.randint(18, 90)
        fr_str = f"{edad} Años"
        fc = random.randint(50, 120) 
        fc_str = f"{fc:03d}ppm"
        spo2 = random.randint(85, 100)
        spo2_str = f"{spo2}%"
        registros.append({
            "id": id_str,
            "fr": fr_str,
            "fc": fc_str,
            "spo2": spo2_str
        })
    return registros

def ordenar_por_fc(registros):
    """
    Ordena por frecuencia cardiaca (extrae número de '090ppm').
    """
    def extraer_fc(reg):
        try:
            return int(reg['fc'].replace('ppm', ''))
        except Exception:
            return float('inf')
    return sorted(registros, key=extraer_fc)
