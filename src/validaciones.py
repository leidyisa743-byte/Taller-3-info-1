import re

def validar_patrones(registro):
    """
    Item 4: Validación con expresiones regulares.
    Verifica que cada campo cumpla el formato estricto.
    """
    patrones = {
        # ID-001 (ID- seguido de 3 dígitos)
        "id": r"^ID-\d{3}$",
        # 18 Años (1 o 2 dígitos, espacio, Años)
        "fr": r"^\d{1,2} Años$",
        # 090ppm (3 dígitos exactos, ppm)
        "fc": r"^\d{3}ppm$",
        # 95% (1 a 3 dígitos, %)
        "spo2": r"^\d{1,3}%$"
    }

    errores = []
    for campo, patron in patrones.items():
        valor = registro.get(campo, "")
        if not re.match(patron, valor):
            errores.append(campo)
    
    return len(errores) == 0