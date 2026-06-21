# database/connection.py
import psycopg2

# Configuración de los parámetros de conexión
DB_HOST = "localhost"         
DB_NAME = "gestor_horas_extension" 
DB_USER = "horas_ext_user"          
DB_PASSWORD = "password"   
DB_PORT = "5432"              

def obtener_conexion():
    """
    Establece y retorna una conexión activa a la base de datos PostgreSQL.
    Cada DAO llamará a esta función cuando necesite operar.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error crítico al intentar conectar con la base de datos: {e}")
        # Si la conexión falla, levantamos la excepción para que el DAO sepa que no hay sistema
        raise e
    



'''
En esencia, la conexión encapsula una sesión de base de datos, 
y te permite ejecutar comandos y consultas SQL, como SELECT, INSERT, 
CREATE, UPDATE, o DELETE, utilizando el método cursor(), y hacer 
cambios persistentes utilizando el método commit() .

Una vez creada la instancia del cursor, puedes 
enviar comandos a la base de datos utilizando el método 
execute() y recuperar datos de una tabla utilizando fetchone(), 
fetchmany()o fetchall().

Por último, es importante que cierres el cursor y 
la conexión con la base de datos cuando hayas terminado 
tus operaciones. De lo contrario, seguirán reteniendo recursos 
del lado del servidor. Para ello, puedes utilizar elmétodo close() .
'''