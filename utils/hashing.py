import hashlib

def calcular_hashing(texto_plano):
    texto_bytes = texto_plano.encode('utf-8')

    objeto_hash = hashlib.sha256(texto_bytes)

    hash_resultado = objeto_hash.hexdigest()

    return hash_resultado
