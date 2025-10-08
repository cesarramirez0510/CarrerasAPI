import mysql.connector
from mysql.connector import Error
from carrera import Carrera

class CarreraDAO:
    def __init__(self, db_user, db_password, db_port):
        self.db_user = db_user
        self.db_password = db_password
        self.db_port = db_port
        self.host = "localhost"
        self.database = "gestioncarrera"
    
    def _conectar(self):
        try:
            return mysql.connector.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.host,
                database=self.database,
                port=self.db_port
            )
        except Error as e:
            print(f"Error conectando a MySQL: {e}")
            return None
    
    def obtener_por_id(self, id_carrera):
        conn = self._conectar()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM carrera WHERE idCarrera = %s", (id_carrera,))
            resultado = cursor.fetchone()
            
            if resultado:
                carrera = Carrera()
                carrera.set_id_carrera(resultado[0])
                carrera.set_nombre_carrera(resultado[1])
                carrera.set_duracion(resultado[2])
                return carrera
            return None
        except Error as e:
            raise Exception(f"Error al obtener carrera: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def obtener_todas(self):
        conn = self._conectar()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM carrera")
            resultados = cursor.fetchall()
            
            carreras = []
            for fila in resultados:
                carrera = Carrera()
                carrera.set_id_carrera(fila[0])
                carrera.set_nombre_carrera(fila[1])
                carrera.set_duracion(fila[2])
                carreras.append(carrera)
            return carreras
        except Error as e:
            raise Exception(f"Error al obtener carreras: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def insertar(self, carrera):
        conn = self._conectar()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor()
            sql = "INSERT INTO carrera (nombrecarrera, duracion) VALUES (%s, %s)"
            cursor.execute(sql, (carrera.get_nombre_carrera(), carrera.get_duracion()))
            conn.commit()
            carrera.set_id_carrera(cursor.lastrowid)
            return carrera
        except Error as e:
            raise Exception(f"Error al insertar carrera: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def actualizar(self, carrera):
        conn = self._conectar()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM carrera WHERE idCarrera = %s", (carrera.get_id_carrera(),))
            if not cursor.fetchone():
                return False
            
            sql = "UPDATE carrera SET nombrecarrera = %s, duracion = %s WHERE idCarrera = %s"
            cursor.execute(sql, (carrera.get_nombre_carrera(), carrera.get_duracion(), carrera.get_id_carrera()))
            conn.commit()
            return True
        except Error as e:
            raise Exception(f"Error al actualizar carrera: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def eliminar(self, id_carrera):
        conn = self._conectar()
        if not conn:
            raise Exception("Error de conexión a la base de datos")
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM carrera WHERE idCarrera = %s", (id_carrera,))
            if not cursor.fetchone():
                return False
            
            sql = "DELETE FROM carrera WHERE idCarrera = %s"
            cursor.execute(sql, (id_carrera,))
            conn.commit()
            return True
        except Error as e:
            raise Exception(f"Error al eliminar carrera: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
    
    def verificar_conexion(self):
        conn = self._conectar()
        if conn and conn.is_connected():
            conn.close()
            return True
        return False