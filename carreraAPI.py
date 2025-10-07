from flask import Flask, jsonify, request
import mysql.connector


app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        user="root",
        password="123456",
        host="localhost",
        database="gestioncarrera",
        port="3307"
    )

@app.route('/carreras/<int:idCarrera>', methods=['GET'])
def obtener_carrera(idCarrera):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM carrera WHERE idCarrera = %s", (idCarrera,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        carrera = {
            "idCarrera": resultado[0],
            "nombrecarrera": resultado[1],
            "duracion": resultado[2]
        }
        return jsonify(carrera)
    else:
        return jsonify({"mensaje": f"No se encontró carrera con ID {idCarrera}"}), 404

@app.route('/carreras', methods=['GET'])
def obtener_todas_las_carreras():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM carrera")
    resultados = cursor.fetchall()
    conn.close()

    carreras = []
    for fila in resultados:
        carrera = {
            "idCarrera": fila[0],
            "nombrecarrera": fila[1],
            "duracion": fila[2]
        }
        carreras.append(carrera)

    return jsonify(carreras)

@app.route('/carreras', methods=['POST'])
def insertar_carrera():
    datos = request.json
    nombre = datos['nombrecarrera']
    duracion = datos['duracion']

    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO carrera (nombrecarrera, duracion) VALUES (%s, %s)"
    cursor.execute(sql, (nombre, duracion))
    conn.commit()

    nuevo_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "mensaje": f'Carrera "{nombre}" insertada correctamente',
        "idCarrera": nuevo_id
    })


@app.route('/carrera/<int:idCarrera>', methods=['PUT'])
def actualizar_carrera(idCarrera):
    datos = request.json
    nuevo_nombre = datos['nombrecarrera']
    nueva_duracion = datos['duracion']

    conn = conectar()
    cursor = conn.cursor()
    sql = "UPDATE carrera SET nombrecarrera = %s, duracion = %s WHERE idCarrera = %s"
    cursor.execute(sql, (nuevo_nombre, nueva_duracion, idCarrera))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": f'Carrera con ID {idCarrera} actualizada correctamente'})

@app.route('/carrera/<int:idCarrera>', methods=['DELETE'])
def eliminar_carrera(idCarrera):
    conn = conectar()
    cursor = conn.cursor()
    sql = "DELETE FROM carrera WHERE idCarrera = %s"
    cursor.execute(sql, (idCarrera,))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": f'Carrera con ID {idCarrera} eliminada correctamente'})

if __name__ == '__main__':
    app.run(debug=True)