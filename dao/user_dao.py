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

        hash_guardado = #la respuesta sql
        hash_ingresado = utils.hashing(password) #la funcion de hashing todavia no tengo

        usuario_valido = True
        while usuario_valido :
            if hash_guardado == hash_ingresado:
                usuario_valido = False 
            