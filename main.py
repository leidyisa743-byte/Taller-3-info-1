import sys
from src.configuracion import CANTIDAD_REGISTROS
from src.generador import generar_datos_aleatorios, ordenar_por_fc
from src.gestor_archivos import crear_carpetas, guardar_archivos, leer_json_local, registrar_log
from src.validaciones import validar_patrones
from src.base_datos import insertar_datos_mongo, ejecutar_consultas

def menu():
    datos_en_memoria = []

    # Inicializar sistema (Item 3)
    crear_carpetas()

    while True:
        print("\n--- TALLER BIOINGENIERÍA: GESTIÓN DE DATOS ---")
        print("1. Generar y Ordenar Datos (Memoria)")
        print("2. Guardar archivos (TXT, CSV, JSON)")
        print("3. Validar Datos (Regex)")
        print("4. Cargar a MongoDB Atlas")
        print("5. Consultar MongoDB y Exportar")
        print("6. Salir")
        
        opcion = input("Seleccione: ")

        if opcion == "1":
            raw_datos = generar_datos_aleatorios(CANTIDAD_REGISTROS)
            datos_en_memoria = ordenar_por_fc(raw_datos)
            print(f"Generados {len(datos_en_memoria)} registros y ordenados por FC.")
            # Mostrar primer registro como ejemplo
            print(f"Ejemplo: {datos_en_memoria[0]}")
            registrar_log("Datos generados y ordenados en memoria.")

        elif opcion == "2":
            if not datos_en_memoria:
                print("Primero genere los datos (Opción 1).")
            else:
                guardar_archivos(datos_en_memoria)
                print("Datos guardados en carpeta /datos")

        elif opcion == "3":
            if not datos_en_memoria:
                print("Primero genere los datos.")
            else:
                validos = 0
                for doc in datos_en_memoria:
                    if validar_patrones(doc):
                        validos += 1
                print(f"Validación completada. Registros válidos: {validos}/{len(datos_en_memoria)}")
                registrar_log(f"Validación regex ejecutada: {validos} correctos.")

        elif opcion == "4":
            # Intentamos leer del JSON local si no hay en memoria
            if not datos_en_memoria:
                datos_en_memoria = leer_json_local()
            
            if datos_en_memoria:
                # Insertar solo los válidos
                datos_para_mongo = [d for d in datos_en_memoria if validar_patrones(d)]
                insertar_datos_mongo(datos_para_mongo)
            else:
                print("No hay datos para cargar. Genere (1) o Importe (automático al intentar cargar).")

        elif opcion == "5":
            ejecutar_consultas()

        elif opcion == "6":
            print("Saliendo...")
            sys.exit()
        else:
            print("Opción inválida.")

if __name__ == "__main__":
    menu()