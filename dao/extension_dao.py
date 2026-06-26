import psycopg2
from database.conection import obtener_conexion

class HorasExtensionDAO:
    @classmethod
    def obtener_profesores_dict(cls):
        query = """
            SELECT DISTINCT u.id_user, u.nombre 
            FROM usuarios u
            WHERE u.rol = 'profesor'
            ORDER BY u.nombre ASC;
        """
        conn = obtener_conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return {nombre: id_user for id_user, nombre in cursor.fetchall()}
        except psycopg2.Error as e:
            print(f"Error al obtener profesores: {e}")
            return {}
        finally:
            conn.close()

    @classmethod
    def obtener_actividades_dict(cls):
        query = "SELECT id_acti, tipo, subtipo FROM actividades;"
        conn = obtener_conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return {f"{tipo} ({subtipo})": id_acti for id_acti, tipo, subtipo in cursor.fetchall()}
        except psycopg2.Error as e:
            print(f"Error al obtener actividades: {e}")
            return {}
        finally:
            conn.close()

    @classmethod
    def agregar_horas(cls, horas_ext):
        sql = """
            INSERT INTO horas_extension 
            (alumno_id, semestre, ubicacion, materia_id, profesor_id, fecha, horas, informe)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        conn = obtener_conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (
                    horas_ext.alumno_id, horas_ext.semestre, horas_ext.ubicacion,
                    horas_ext.materia_id, horas_ext.profesor_id,
                    horas_ext.fecha, horas_ext.horas, horas_ext.informe
                ))
                conn.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error al insertar horas en BD: {e}")
            conn.rollback()
            return False
        finally:
            conn.close()

    @classmethod
    def obtener_resumen_alumno(cls, alumno_id):
        """Devuelve todas las actividades registradas por un estudiante específico"""
        sql = """
            SELECT h.fecha, h.semestre, h.ubicacion, m.nombre, u.nombre, h.horas, h.informe
            FROM horas_extension h
            LEFT JOIN materias m ON h.materia_id = m.id_materias
            LEFT JOIN usuarios u ON h.profesor_id = u.id_user
            WHERE h.alumno_id = %s
            ORDER BY h.fecha DESC;
        """
        conn = obtener_conexion()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, (alumno_id,))
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error al obtener resumen de horas: {e}")
            return []
        finally:
            conn.close()