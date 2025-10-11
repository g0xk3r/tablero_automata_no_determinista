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

def tam_cadena(eleccion):
    if eleccion == 1:
        lista_cadenas = [''.join(random.choices('rb', k=long_cadena)) for _ in range(3)]
        return lista_cadenas.lower()

def pedir_cadena(long_cadena):
    string = input(f"Ingrese la cadena con longitud {long_cadena}: ")
    if len(string) == long_cadena:
        return string.lower()
    else:
        print("La cadena no tiene la longitud correcta.")
        return pedir_cadena(long_cadena)

if __name__ == "__main__":
    option = menu()
    if option == 1:
        cadenas = tam_cadena(option)
    elif option == 2:
        cadenas = tam_cadena(option)
        long_cadena = int(input("Tamaño de la cadena: "))