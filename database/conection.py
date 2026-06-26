import psycopg2

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="gestion_hora_extension_prueba", #cambien por el nombre de su base de datos local
            user="postgres",
            password="Tyopt203", #cambien por su contraseña
            port="5432"
        )

        return conexion
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None
