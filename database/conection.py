import psycopg2

def obtener_conexion():
    try:
        conexion = psycopg2.connect(
            host="localhost",
            database="gestion_hora_extension", # La que creaste en pgAdmin4
            user="postgres",
            password="Tyopt203", # Contraseña del pgAdmin4 local
            port="5432"
        )
        return conexion
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")