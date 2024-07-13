import datetime

class Evento:
    def __init__(self, nombre: str, fecha: datetime, duracion: int, num_participantes: int, num_jueces: int):
        self.nombre = nombre
        self.fecha = fecha
        self.duracion = duracion
        self.num_participantes = num_participantes
        self.num_jueces = num_jueces