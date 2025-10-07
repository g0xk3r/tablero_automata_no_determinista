import random

long_cadena = int(input("Tamaño de la cadena: "))

def pedir_cadena(long_cadena):
    string = input(f"Ingrese la cadena con longitud {long_cadena}: ")
    if len(string) == long_cadena:
        return string.lower()
    else:
        print("La cadena no tiene la longitud correcta.")
        return pedir_cadena(long_cadena)

