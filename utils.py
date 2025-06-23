
import random

def simular_digitos():
    return [random.randint(0, 9) for _ in range(10)]

def simular_coletas(n=3):
    return [simular_digitos() for _ in range(n)]
