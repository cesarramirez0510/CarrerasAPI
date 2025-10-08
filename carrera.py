class Carrera:
    def __init__(self, id_carrera=None, nombre_carrera=None, duracion=None):
        self.__id_carrera = id_carrera
        self.__nombre_carrera = nombre_carrera
        self.__duracion = duracion

    def get_id_carrera(self):
        return self.__id_carrera
    
    def set_id_carrera(self, valor):
        self.__id_carrera = valor
    
    def get_nombre_carrera(self):
        return self.__nombre_carrera
    
    def set_nombre_carrera(self, valor):
        self.__nombre_carrera = valor
    
    def get_duracion(self):
        return self.__duracion
    
    def set_duracion(self, valor):
        self.__duracion = valor