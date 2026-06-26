import psycopg2

class HorasExtensionDAO:
    @classmethod
    def obtener_profesores_dict(cls, connection):
        """Trae el nombre y ID de los profesores."""
        query = """
            SELECT DISTINCT u.id_user, u.nombre 
            FROM usuarios u
            JOIN profesor_materias pm ON u.id_user = pm.profesor_id
            WHERE u.rol = 'profesor'
            ORDER BY u.nombre ASC;
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                # Creamos el diccionario: {nombre: id_user}
                return {nombre: id_user for id_user, nombre in cursor.fetchall()}
        except psycopg2.Error as e:
            print(f"Error al obtener profesores: {e}")
            return {}

    @classmethod
    def obtener_actividades_dict(cls, connection):
        """Trae las actividades usando id_acti."""
        query = "SELECT id_acti, tipo, subtipo FROM actividades;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                # Creamos el diccionario: {tipo (subtipo): id_acti}
                return {f"{tipo} ({subtipo})": id_acti for id_acti, tipo, subtipo in cursor.fetchall()}
        except psycopg2.Error as e:
            print(f"Error al obtener actividades: {e}")
            return {}

    @classmethod
    def agregar_horas(cls, connection, horas_ext, es_prueba=False):
        try:
            with connection.cursor() as cursor:
                sql = """
                    INSERT INTO horas_extension 
                    (alumno_id, semestre, ubicacion, materia_id, profesor_id, actividad_id, fecha, horas, descripcion)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(sql, (
                    horas_ext.alumno_id, horas_ext.semestre, horas_ext.ubicacion,
                    horas_ext.materia_id, horas_ext.profesor_id, horas_ext.actividad_id,
                    horas_ext.fecha, horas_ext.horas, horas_ext.informe
                ))
                connection.commit()
                return True
        except psycopg2.Error as e:
            print(f"Error al insertar horas: {e}")
            connection.rollback()
            return False