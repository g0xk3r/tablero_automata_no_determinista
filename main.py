import random
from tablero import Tablero
from jugador import Jugador
from juego import Juego

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
        print(f"Tamaño de las cadenas (3 - 100): {tam}")
        return tam
    else:
        long_cadena = int(input("Tamaño de las cadenas (3 - 100): "))
        return long_cadena

def pedir_cadena(long_cadena, eleccion):
    if eleccion == 1:
        cadena = ''.join(random.choice('rb') for _ in range(long_cadena))
        print(f"Ingrese la cadena con longitud {long_cadena}: {cadena}")
        print("Cadena generada.")
        return cadena
    else:
        string = input(f"Ingrese la cadena con longitud {long_cadena}: ")
        if len(string) == long_cadena:
            print("Cadena generada.")
            return string.lower()
        else:
            print("La cadena no tiene la longitud correcta.")
            return pedir_cadena(long_cadena)

def reconfiguracion_cadena(cadena_original):
    cadena_sin_ultimo = cadena_original[:-1]
    ultimo_caracter = cadena_original[-1]
    if ultimo_caracter == 'r':
        cadena_j2 = cadena_original
        cadena_j_1_3 = cadena_sin_ultimo + 'b'
    else:
        cadena_j2 = cadena_sin_ultimo + 'r'
        cadena_j_1_3 = cadena_original
    return {
        1: cadena_j_1_3,
        2: cadena_j2,
        3: cadena_j_1_3
    }

if __name__ == "__main__":
    option = menu()
    if option != 0:
        long_cadena = pedir_tam_cadena(option)
        cadena_original = pedir_cadena(long_cadena, option)
        print("Cadena ingresada:", cadena_original)
        nuevas_cadenas = reconfiguracion_cadena(cadena_original)
        for i in range(1, 4):
            print(f"Cadena para el jugador {i}: {nuevas_cadenas[i]}")
        tablero = Tablero(4, 4)
        jugadores = [
            Jugador(1, 1, 16),
            Jugador(2, 4, 13),
            Jugador(3, 3, 14)
        ]
        num_movimientos = long_cadena
        for jugador in jugadores:
            cadena_correspondiente = nuevas_cadenas[jugador.id]
            jugador.creacion_rutas(num_movimientos, tablero, cadena_correspondiente)

        juego_visual = Juego(tablero, jugadores, num_movimientos)
        juego_visual.asignar_rutas_aleatorias()
        juego_visual.iniciar_partida()
    else:
        print("Programa terminado.")