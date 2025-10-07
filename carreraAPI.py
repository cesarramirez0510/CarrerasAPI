from flask import Flask, jsonify, request
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

db_user = None
db_password = None
db_port = None

def conectar():
    """Crea una conexión MySQL usando las credenciales del inicio de sesión."""
    try:
        return mysql.connector.connect(
            user=db_user,
            password=db_password,
            host="localhost",
            database="gestioncarrera",
            port=db_port
        )
    except Error as e:
        print(f"Error conectando a MySQL: {e}")
        return None
    
@app.route('/carreras/<int:idCarrera>', methods=['GET'])
def obtener_carrera(idCarrera):
    conn = conectar()
    if not conn:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM carrera WHERE idCarrera = %s", (idCarrera,))
        resultado = cursor.fetchone()
        
        if resultado:
            carrera = {
                "idCarrera": resultado[0],
                "nombrecarrera": resultado[1],
                "duracion": resultado[2]
            }
            return jsonify(carrera), 200
        else:
            return jsonify({"mensaje": f"No se encontró carrera con ID {idCarrera}"}), 404
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/carreras', methods=['GET'])
def obtener_todas_las_carreras():
    conn = conectar()
    if not conn:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM carrera")
        resultados = cursor.fetchall()
        
        carreras = []
        for fila in resultados:
            carrera = {
                "idCarrera": fila[0],
                "nombrecarrera": fila[1],
                "duracion": fila[2]
            }
            carreras.append(carrera)
        return jsonify(carreras), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/carreras', methods=['POST'])
def insertar_carrera():
    datos = request.json
    
    if not datos or 'nombrecarrera' not in datos or 'duracion' not in datos:
        return jsonify({"error": "Datos incompletos"}), 400
    
    nombre = datos['nombrecarrera']
    duracion = datos['duracion']
    
    if not nombre or not isinstance(duracion, int) or duracion <= 0:
        return jsonify({"error": "Datos inválidos"}), 400
    
    conn = conectar()
    if not conn:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    try:
        cursor = conn.cursor()
        sql = "INSERT INTO carrera (nombrecarrera, duracion) VALUES (%s, %s)"
        cursor.execute(sql, (nombre, duracion))
        conn.commit()
        nuevo_id = cursor.lastrowid
        
        return jsonify({
            "mensaje": f'Carrera "{nombre}" insertada correctamente',
            "idCarrera": nuevo_id
        }), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/carreras/<int:idCarrera>', methods=['PUT'])
def actualizar_carrera(idCarrera):
    datos = request.json
    
    if not datos or 'nombrecarrera' not in datos or 'duracion' not in datos:
        return jsonify({"error": "Datos incompletos"}), 400
    
    nuevo_nombre = datos['nombrecarrera']
    nueva_duracion = datos['duracion']
    
    conn = conectar()
    if not conn:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM carrera WHERE idCarrera = %s", (idCarrera,))
        if not cursor.fetchone():
            return jsonify({"mensaje": f"No existe carrera con ID {idCarrera}"}), 404
        
        sql = "UPDATE carrera SET nombrecarrera = %s, duracion = %s WHERE idCarrera = %s"
        cursor.execute(sql, (nuevo_nombre, nueva_duracion, idCarrera))
        conn.commit()
        
        return jsonify({"mensaje": f'Carrera con ID {idCarrera} actualizada correctamente'}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

@app.route('/carreras/<int:idCarrera>', methods=['DELETE'])
def eliminar_carrera(idCarrera):
    conn = conectar()
    if not conn:
        return jsonify({"error": "Error de conexión a la base de datos"}), 500
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM carrera WHERE idCarrera = %s", (idCarrera,))
        if not cursor.fetchone():
            return jsonify({"mensaje": f"No existe carrera con ID {idCarrera}"}), 404
        
        sql = "DELETE FROM carrera WHERE idCarrera = %s"
        cursor.execute(sql, (idCarrera,))
        conn.commit()
        
        return jsonify({"mensaje": f'Carrera con ID {idCarrera} eliminada correctamente'}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def login_mysql():
    global db_user, db_password, db_port

    print("\n" + "=" * 60)
    print("CONFIGURACIÓN DE CONEXIÓN A MySQL")
    print("=" * 60)

    while True:
        db_user = input("Usuario MySQL: ").strip()
        db_password = input("Contraseña MySQL: ").strip()
        db_port = input("Puerto MySQL: ").strip()

        print("\nVerificando conexión...\n")
        conn = conectar()
        if conn and conn.is_connected():
            print("Conexión exitosa a MySQL.")
            conn.close()
            break
        else:
            print("No se pudo conectar. Verifica los datos e inténtalo nuevamente.\n")
            retry = input("¿Intentar otra vez? (s/n): ").lower()
            if retry != "s":
                print("\nSaliendo del programa...\n")
                exit()
      

if __name__ == '__main__':
    login_mysql()
    print("\nIniciando servidor Flask...\n")
    app.run(debug=True)