
from database.conection import obtener_conexion
from utils.hashing import calcular_hashing
from models.user import User 

#import libreria para conectar a postgers - no tengo todavia

class UserDAO:
    #Verificar existencia del usuario
    @classmethod
    def usuario_existe(cls, nombre):
        sql = ("SELECT COUNT(*) FROM usuarios WHERE nombre = %s")
        conn = obtener_conexion()
        try: 
            with conn.cursor() as cur:
                cur.execute(sql, (nombre,))
                registro = cur.fetchone()

                if registro:
                    return registro[0] > 0
                return False

        except Exception as e:
            print(f"Error en el proceso de Crear Usuario: {e}")
            return False
        finally: 
            conn.close()



    #CREATE USER ========================
    @classmethod
    def crear_usuario(cls, nombre, password):
        if cls.crear_usuario(nombre):
            print(f"El usuario con el nombre {nombre} ya existe. No se puede crear")
            return False
        
        sql = ("INSERT INTO usuarios(nombre, password) VALUES(%s, %s)")
        conn = obtener_conexion()

        try:
            with conn.cursor() as cur:
                password_Hasheado = calcular_hashing(password)

                cur.execute(sql, (nombre, password_Hasheado))
                conn.commit()
                print(f"Usuario {nombre} creado con exito!")
                return True
            

        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            return False
        finally: 
            conn.close()


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


            