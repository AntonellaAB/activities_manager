from database.conection import obtener_conexion
from utils.hashing import calcular_hashing
from models.user import User 

class UserDAO:
    @classmethod
    def usuario_existe(cls, nombre):
        sql = "SELECT COUNT(*) FROM usuarios WHERE nombre = %s"
        conn = obtener_conexion()
        try: 
            with conn.cursor() as cur:
                cur.execute(sql, (nombre,))
                registro = cur.fetchone()
                return registro[0] > 0 if registro else False
        except Exception as e:
            print(f"Error al verificar existencia de usuario: {e}")
            return False
        finally: 
            conn.close()

    @classmethod
    def crear_usuario(cls, nombre, email, password, rol='estudiante'):
        if cls.usuario_existe(nombre):
            print(f"El usuario con el nombre {nombre} ya existe. No se puede crear")
            return False
        
        sql = "INSERT INTO usuarios(nombre, email, password_hash, rol) VALUES(%s, %s, %s, %s)"
        conn = obtener_conexion()
        try:
            with conn.cursor() as cur:
                password_hasheado = calcular_hashing(password)
                cur.execute(sql, (nombre, email, password_hasheado, rol))
                conn.commit()
                print(f"Usuario {nombre} creado con éxito!")
                return True
        except Exception as e:
            print(f"Error al insertar usuario: {e}")
            return False
        finally: 
            conn.close()

    @classmethod
    def login(cls, nombre, password):
        sql = "SELECT id_user, nombre, password_hash, rol FROM usuarios WHERE nombre = %s"
        conn = obtener_conexion()
        try: 
            with conn.cursor() as cur:
                cur.execute(sql, (nombre,))
                registro = cur.fetchone()
                if registro:
                    id_db, nombre_db, hash_db, rol_db = registro
                    password_hasheado = calcular_hashing(password)
                    if password_hasheado == hash_db:
                        return User(id_user=id_db, nombre=nombre_db, rol=rol_db)
            return None
        except Exception as e:
            print(f"Error en el proceso de login: {e}")
            return None
        finally: 
            conn.close()