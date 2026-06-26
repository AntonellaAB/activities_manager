# Archivo: dao/materias_dao.py
import psycopg2
from models.materias import Subject

class SubjectDAO:
    @classmethod
    def get_all(cls, connection):
        subjects = []
        try:
            with connection.cursor() as cursor:
                # Usamos id_materias
                cursor.execute("SELECT id_materias, nombre FROM materias ORDER BY nombre ASC;")
                records = cursor.fetchall()
                for record in records:
                    subjects.append(Subject(subject_id=record[0], name=record[1]))
        except psycopg2.Error as e:
            print(f"Error al obtener materias: {e}")
        return subjects

    @classmethod
    def insert(cls, connection, subject: Subject):
        try:
            with connection.cursor() as cursor:
                # Retornamos id_materias
                sql = "INSERT INTO materias (nombre) VALUES (%s) RETURNING id_materias;"
                cursor.execute(sql, (subject.name,))
                generated_id = cursor.fetchone()[0]
                connection.commit()
                subject.subject_id = generated_id
                return True
        except psycopg2.Error as e:
            print(f"Error al insertar materia: {e}")
            connection.rollback()
            return False

    @classmethod
    def get_by_id(cls, connection, subject_id):
        try:
            with connection.cursor() as cursor:
                # Buscamos por id_materias
                sql = "SELECT id_materias, nombre FROM materias WHERE id_materias = %s;"
                cursor.execute(sql, (subject_id,))
                record = cursor.fetchone()
                if record:
                    return Subject(subject_id=record[0], name=record[1])
        except psycopg2.Error as e:
            print(f"Error al obtener la materia: {e}")
        return None