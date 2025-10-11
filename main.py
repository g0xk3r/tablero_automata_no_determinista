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

def pedir_tam_cadena(eleccion):
    if eleccion == 1:
        random.seed()
        tam = random.randint(3, 100)
        print(f"Tamaño de las cadenas: {tam}")
        return tam
    else:
        long_cadena = int(input("Tamaño de las cadenas: "))
        return long_cadena

def pedir_cadena(long_cadena, eleccion):
    if eleccion == 1:
        cadena = ''.join(random.choice('rb') for _ in range(long_cadena))
        print(f"Ingrese la cadena con longitud {long_cadena}: {cadena}")
        print("Cadena generada exitosamente.")
        return cadena
    else:
        string = input(f"Ingrese la cadena con longitud {long_cadena}: ")
        if len(string) == long_cadena:
            print("Cadena generada exitosamente.")
            return string.lower()
        else:
            print("La cadena no tiene la longitud correcta.")
            return pedir_cadena(long_cadena)

if __name__ == "__main__":
    option = menu()
    if option != 0:
        long_cadena = pedir_tam_cadena(option)
        cadenas = [pedir_cadena(long_cadena, option) for _ in range(3)]
        print("Cadenas ingresadas:", cadenas)
    else:
        print("Programa terminado.")