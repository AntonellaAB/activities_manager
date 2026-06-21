
from database.conection import obtener_conexion
from utils.hashing import calcular_hashing
from models.user import User 

#import libreria para conectar a postgers - no tengo todavia

class UserDAO:
    
    #CREATE USER ========================
    def crear_usuario():
        pass 


    #LOGIN ===============================
    @classmethod
    def login(cls, nombre, password):
        #hacer consulta sql 
        sql = ("SELECT id_user, nombre, password_hash, rol FROM usuarios WHERE nombre = %s")

        #pedimos la conexion 
        conn = obtener_conexion()
        
        try: 
            with conn.cursor() as cur:
                cur.execute(sql, (nombre,))
                registro = cur.fetchone()

                if registro:
                    id_db, nombre_db, hash_db, rol_db = registro

                    password = calcular_hashing(password)

                    if password == hash_db:
                        return User(id_user=id_db, nombre=nombre_db, rol=rol_db)
            
            return None

        except Exception as e:
            print(f"Error en el proceso de login: {e}")
            return None
        
        finally: 
            conn.close()


            