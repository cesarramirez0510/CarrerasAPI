import requests

BASE_URL = "http://127.0.0.1:5000"

def mostrar_carreras():
    response = requests.get(f"{BASE_URL}/carreras")
    if response.status_code == 200:
        carreras = response.json()
        print("Carreras registradas:")
        for c in carreras:
            print(f'ID: {c["idCarrera"]} | Nombre: {c["nombrecarrera"]} | Duración: {c["duracion"]} años')
    else:
        print("Error al obtener las carreras")

def insertar_carrera():
    nombre = input("Nombre de la carrera: ")
    duracion = int(input("Duración (años): "))
    datos = {
        "nombrecarrera": nombre,
        "duracion": duracion
    }
    response = requests.post(f"{BASE_URL}/carreras", json=datos)
    print(response.json())

def actualizar_carrera():
    idCarrera = int(input("ID de la carrera a actualizar: "))
    nuevo_nombre = input("Nuevo nombre: ")
    nueva_duracion = int(input("Nueva duración: "))
    datos = {
        "nombrecarrera": nuevo_nombre,
        "duracion": nueva_duracion
    }
    response = requests.put(f"{BASE_URL}/carrera/{idCarrera}", json=datos)
    print(response.json())

def eliminar_carrera():
    idCarrera = int(input("ID de la carrera a eliminar: "))
    response = requests.delete(f"{BASE_URL}/carrera/{idCarrera}")
    print(response.json())


if __name__ == "__main__":
    try:
        while True:
            print("----- Cliente API de gestión de carreras -----")
            print("1 - Mostrar carreras")
            print("2 - Insertar carrera")
            print("3 - Actualizar carrera")
            print("4 - Eliminar carrera")
            print("5 - Salir")
            opcion = int(input("Selecciona una opción (1-5): "))

            if opcion == 1:
                mostrar_carreras()
            elif opcion == 2:
                insertar_carrera()
            elif opcion == 3:
                actualizar_carrera()
            elif opcion == 4:
                eliminar_carrera()
            elif opcion == 5:
                print("¡Hasta luego!")
                break
            else:
                print("Opción no válida")

    except Exception as e:
        print("Error:", e)