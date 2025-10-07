import requests

BASE_URL = "http://127.0.0.1:5000"

def mostrar_carreras():
    try:
        response = requests.get(f"{BASE_URL}/carreras")
        if response.status_code == 200:
            carreras = response.json()
            if carreras:
                print("\n" + "="*60)
                print("CARRERAS REGISTRADAS")
                print("="*60)
                for c in carreras:
                    print(f'ID: {c["idCarrera"]:3d} | Nombre: {c["nombrecarrera"]:30s} | Duración: {c["duracion"]} años')
                print("="*60 + "\n")
            else:
                print("\nNo hay carreras registradas\n")
        else:
            print(f"\nError al obtener las carreras: {response.json()}\n")
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}\n")

def insertar_carrera():
    try:
        nombre = input("Nombre de la carrera: ").strip()
        if not nombre:
            print("\nEl nombre no puede estar vacío\n")
            return
        
        duracion_input = input("Duración (años): ").strip()
        if not duracion_input.isdigit():
            print("\nLa duración debe ser un número entero\n")
            return
        
        duracion = int(duracion_input)
        if duracion <= 0:
            print("\nLa duración debe ser mayor a 0\n")
            return
        
        datos = {
            "nombrecarrera": nombre,
            "duracion": duracion
        }
        
        response = requests.post(f"{BASE_URL}/carreras", json=datos)
        
        if response.status_code == 201:
            print(f"\n{response.json()['mensaje']}\n")
        else:
            print(f"\nError: {response.json()}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}\n")
    except ValueError:
        print("\nEntrada inválida\n")

def actualizar_carrera():
    try:
        idCarrera = int(input("ID de la carrera a actualizar: "))
        nuevo_nombre = input("Nuevo nombre: ").strip()
        nueva_duracion = int(input("Nueva duración: "))
        
        if not nuevo_nombre or nueva_duracion <= 0:
            print("\nDatos inválidos\n")
            return
        
        datos = {
            "nombrecarrera": nuevo_nombre,
            "duracion": nueva_duracion
        }
        
        response = requests.put(f"{BASE_URL}/carreras/{idCarrera}", json=datos)
        
        if response.status_code == 200:
            print(f"\n{response.json()['mensaje']}\n")
        else:
            print(f"\n{response.json()['mensaje']}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}\n")
    except ValueError:
        print("\nEntrada inválida. Asegúrate de ingresar números donde corresponda\n")

def eliminar_carrera():
    try:
        idCarrera = int(input("ID de la carrera a eliminar: "))
        confirmacion = input(f"¿Estás seguro de eliminar la carrera con ID {idCarrera}? (s/n): ").lower()
        
        if confirmacion != 's':
            print("\nOperación cancelada\n")
            return
        
        response = requests.delete(f"{BASE_URL}/carreras/{idCarrera}")
        
        if response.status_code == 200:
            print(f"\n{response.json()['mensaje']}\n")
        else:
            print(f"\n{response.json()['mensaje']}\n")
            
    except requests.exceptions.RequestException as e:
        print(f"\nError de conexión: {e}\n")
    except ValueError:
        print("\nEntrada inválida. Debes ingresar un número\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("SISTEMA DE GESTIÓN DE CARRERAS")
    print("="*60 + "\n")
    
    while True:
        try:
            print("----- MENÚ PRINCIPAL -----")
            print("1 - Mostrar carreras")
            print("2 - Insertar carrera")
            print("3 - Actualizar carrera")
            print("4 - Eliminar carrera")
            print("5 - Salir")
            print("-" * 26)
            
            opcion = input("Selecciona una opción (1-5): ").strip()
            
            if opcion == "1":
                mostrar_carreras()
            elif opcion == "2":
                insertar_carrera()
            elif opcion == "3":
                actualizar_carrera()
            elif opcion == "4":
                eliminar_carrera()
            elif opcion == "5":
                print("\n¡Hasta luego!\n")
                break
            else:
                print("\nOpción no válida. Por favor selecciona un número del 1 al 5\n")
                
        except KeyboardInterrupt:
            print("\n\n¡Hasta luego!\n")
            break
        except Exception as e:
            print(f"\nError inesperado: {e}\n")