import re

def validar_patrones(registro):
    """
    Valida un único registro contra los patrones definidos.
    Devuelve (es_valido: bool, errores: list[str])
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

    return (len(errores) == 0, errores)

def validar_registros(lista_registros):
    """
    Valida una lista de registros y devuelve:
    - validos: lista de registros válidos
    - invalidos: lista de tuples (registro, errores)
    """
    validos = []
    invalidos = []
    for reg in lista_registros:
        ok, errores = validar_patrones(reg)
        if ok:
            validos.append(reg)
        else:
            invalidos.append((reg, errores))
    return validos, invalidos
