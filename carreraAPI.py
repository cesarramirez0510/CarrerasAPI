from flask import Flask, jsonify, request
from carrera import Carrera
from carrera_dao import CarreraDAO

app = Flask(__name__)
carrera_dao = None

@app.route('/carreras/<int:idCarrera>', methods=['GET'])
def obtener_carrera(idCarrera):
    try:
        carrera = carrera_dao.obtener_por_id(idCarrera)
        
        if carrera:
            return jsonify({
                "idCarrera": carrera.get_id_carrera(),
                "nombrecarrera": carrera.get_nombre_carrera(),
                "duracion": carrera.get_duracion()
            }), 200
        else:
            return jsonify({"mensaje": f"No se encontró carrera con ID {idCarrera}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/carreras', methods=['GET'])
def obtener_todas_las_carreras():
    try:
        carreras = carrera_dao.obtener_todas()
        
        resultado = []
        for carrera in carreras:
            resultado.append({
                "idCarrera": carrera.get_id_carrera(),
                "nombrecarrera": carrera.get_nombre_carrera(),
                "duracion": carrera.get_duracion()
            })
        
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/carreras', methods=['POST'])
def insertar_carrera():
    datos = request.json
    
    if not datos or 'nombrecarrera' not in datos or 'duracion' not in datos:
        return jsonify({"error": "Datos incompletos"}), 400
    
    nombre = datos['nombrecarrera']
    duracion = datos['duracion']
    
    if not nombre or not isinstance(duracion, int) or duracion <= 0:
        return jsonify({"error": "Datos inválidos"}), 400
    
    try:
        carrera = Carrera()
        carrera.set_nombre_carrera(nombre)
        carrera.set_duracion(duracion)
        
        carrera_insertada = carrera_dao.insertar(carrera)
        
        return jsonify({
            "mensaje": f'Carrera "{nombre}" insertada correctamente',
            "idCarrera": carrera_insertada.get_id_carrera()
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/carreras/<int:idCarrera>', methods=['PUT'])
def actualizar_carrera(idCarrera):
    datos = request.json
    
    if not datos or 'nombrecarrera' not in datos or 'duracion' not in datos:
        return jsonify({"error": "Datos incompletos"}), 400
    
    nuevo_nombre = datos['nombrecarrera']
    nueva_duracion = datos['duracion']
    
    try:
        carrera = Carrera()
        carrera.set_id_carrera(idCarrera)
        carrera.set_nombre_carrera(nuevo_nombre)
        carrera.set_duracion(nueva_duracion)
        
        actualizado = carrera_dao.actualizar(carrera)
        
        if actualizado:
            return jsonify({"mensaje": f'Carrera con ID {idCarrera} actualizada correctamente'}), 200
        else:
            return jsonify({"mensaje": f"No existe carrera con ID {idCarrera}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/carreras/<int:idCarrera>', methods=['DELETE'])
def eliminar_carrera(idCarrera):
    try:
        eliminado = carrera_dao.eliminar(idCarrera)
        
        if eliminado:
            return jsonify({"mensaje": f'Carrera con ID {idCarrera} eliminada correctamente'}), 200
        else:
            return jsonify({"mensaje": f"No existe carrera con ID {idCarrera}"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def login_mysql():
    global carrera_dao

    print("\n" + "=" * 60)
    print("CONFIGURACIÓN DE CONEXIÓN A MySQL")
    print("=" * 60)

    while True:
        db_user = input("Usuario MySQL: ").strip()
        db_password = input("Contraseña MySQL: ").strip()
        db_port = input("Puerto MySQL: ").strip()

        print("\nVerificando conexión...\n")
        
        carrera_dao = CarreraDAO(db_user, db_password, db_port)
        
        if carrera_dao.verificar_conexion():
            print("Conexión exitosa a MySQL.")
            break
        else:
            print("No se pudo conectar. Verifica los datos e inténtalo nuevamente.\n")
            retry = input("¿Intentar otra vez? (s/n): ").lower()
            if retry != "s":
                print("\nSaliendo del programa...\n")
                exit()

if __name__ == '__main__':
    login_mysql()
    print("\nIniciando servidor...\n")
    app.run(debug=True)