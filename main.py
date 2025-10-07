import random

def menu():
    print("Menu Principal")
    print("1) Correr de manera automatica")
    print("2) Ingresar datos manualmente")
    print("3) Salir")
    opcion = int(input("Seleccione una opcion: "))
    if opcion == 1:
        print("Generando cadena automaticamente...")
        return 1
    elif opcion == 2:
        print("Ingresando datos manualmente...")
        return 2
    elif opcion == 3:
        print("Saliendo del programa...")
        return 0
    else:
        print("Opcion no valida, intente de nuevo.")
        return menu()

long_cadena = int(input("Tamaño de la cadena: "))

def pedir_cadena(long_cadena):
    string = input(f"Ingrese la cadena con longitud {long_cadena}: ")
    if len(string) == long_cadena:
        return string.lower()
    else:
        print("La cadena no tiene la longitud correcta.")
        return pedir_cadena(long_cadena)

if __name__ == "__main__":
    menu()