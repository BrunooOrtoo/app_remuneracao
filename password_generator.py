import random
import string

def generate_random_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(8))
    #Gera uma senha de 8 caracteres
    return password