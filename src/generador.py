import random

def generar_datos_aleatorios(cantidad):
    """
    Item 1: Generar 50 registros biomédicos aleatorios.
    Campos: id, fr (edad), fc (frecuencia), spo2.
    """
    registros = []
    for i in range(1, cantidad + 1):
        # Formato: ID-001
        id_str = f"ID-{i:03d}"
        
        # Formato: 18 Años
        edad = random.randint(18, 90)
        fr_str = f"{edad} Años"
        
        # Formato: 090ppm
        fc = random.randint(50, 120)
        fc_str = f"{fc:03d}ppm"
        
        # Formato: 95%
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
    Item 1: Ordenar los datos por frecuencia cardiaca.
    Extrae el número de '090ppm' para ordenar correctamente.
    """
    # Función lambda para extraer solo los dígitos de '090ppm' y convertir a int
    return sorted(registros, key=lambda x: int(x['fc'].replace('ppm', '')))