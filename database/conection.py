import psycopg2

def obtener_conexion():
    try:
        # Se eliminaron tildes y la letra n especial para evitar errores de codificacion
        conexion = psycopg2.connect(
            host="localhost",
            database="gestion_hora_extension_prueba",
            user="postgres",
            password="Tyopt203",
            port="5432"
        )

        return conexion
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None