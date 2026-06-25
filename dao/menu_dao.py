from database.conection import obtener_conexion

class MenuDAO:
    @classmethod
    def obtener_total_horas(cls, user_id):
        """Consulta la base de datos y suma las horas de extensión de un usuario."""
        sql = "SELECT COALESCE(SUM(horas), 0) FROM horas_extension WHERE alumno_id = %s;"
        conn = obtener_conexion()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, (user_id,))
                resultado = cur.fetchone()
                return resultado[0] if resultado else 0
        except Exception as e:
            print(f"Error al calcular las horas en MenuDAO: {e}")
            return "Error"
        finally:
            conn.close()