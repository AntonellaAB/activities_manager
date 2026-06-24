# Archivo: models/materias.py

class Subject:
    def __init__(self, subject_id=None, name=""):
        """
        Modelo que representa la tabla 'materias'.
        :param subject_id: int (SERIAL en la BD)
        :param name: str (Nombre de la carrera/materia)
        """
        self.subject_id = subject_id
        self.name = name

    def __str__(self):
        return f"Subject({self.subject_id}): {self.name}"