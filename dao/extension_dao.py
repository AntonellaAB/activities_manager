import psycopg2

class HorasExtensionDAO:
    
    @classmethod
    def agregar_horas(cls, connection, horas_obj, es_prueba=False):
        """
        Inserta un nuevo registro utilizando el objeto del modelo HorasExtension.
        """
        query = """
            INSERT INTO horas_extension (
                alumno_id, semestre, ubicacion, materia_id, 
                profesor_id, actividad_id, fecha, horas, descripcion
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        try:
            with connection.cursor() as cursor:
                # Extraemos los atributos directamente desde el objeto del modelo
                cursor.execute(query, (
                    horas_obj.alumno_id,
                    horas_obj.semestre,
                    horas_obj.ubicacion,
                    horas_obj.materia_id,
                    horas_obj.profesor_id,
                    horas_obj.actividad_id,
                    horas_obj.fecha,
                    horas_obj.horas,
                    horas_obj.informe  # 'informe' en tu modelo mapea a 'descripcion' en SQL
                ))
                id_generado = cursor.fetchone()[0]
                
                if es_prueba:
                    connection.rollback()
                    print(f"[MODO PRUEBA] Simulación exitosa. ID ficticio: {id_generado}. Rollback realizado.")
                else:
                    connection.commit()
                    horas_obj.id = id_generado  # Guardamos el ID real asignado por la BD
                
                return True
        except psycopg2.Error as e:
            connection.rollback()
            print(f"Error al intentar guardar las horas: {e}")
            return False

    @classmethod
    def obtener_profesores_dict(cls, connection):
        """Trae de la BD los usuarios con rol 'profesor' y devuelve un diccionario {Nombre: ID}."""
        query = "SELECT id_user, nombre FROM usuarios WHERE rol = 'profesor' ORDER BY nombre ASC;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return {nombre: id_user for id_user, nombre in cursor.fetchall()}
        except psycopg2.Error as e:
            print(f"Error al obtener profesores: {e}")
            return {}

    @classmethod
    def obtener_actividades_dict(cls, connection):
        """Trae las actividades de la BD y mapea el texto visual 'TIPO (subtipo)' a su ID."""
        query = "SELECT id_acti, tipo, subtipo FROM actividades;"
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                return {f"{tipo} ({subtipo})": id_acti for id_acti, tipo, subtipo in cursor.fetchall()}
        except psycopg2.Error as e:
            print(f"Error al obtener actividades: {e}")
            return {}