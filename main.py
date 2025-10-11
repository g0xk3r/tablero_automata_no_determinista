import random

class Tablero:
    def __init__(self, filas, columnas):
        self.filas = filas
        self.columnas = columnas
        total_casillas = filas * columnas
        self.estados_posibles = list(range(1,total_casillas + 1)) # Estados del 1 al 16
        self.transiciones = self.generar_transiciones()

    def casilla_a_coordenadas(self, casilla):
        fila = (casilla - 1) // self.columnas # Filas completas hasta llegar a la fila
        columna = (casilla - 1) % self.columnas # "Pasos" dados hasta llegar a la columna
        return (fila, columna)

    def coordenada_a_casilla(self, fila, columna):
        return fila * self.columnas + columna + 1 # Casillas totales que se han pasado + pasos dados hasta llegar a la columna + 1

    def generar_transiciones(self):
        transiciones_posibles = {casilla: set() for casilla in self.estados_posibles} # Diccionario con conjuntos vacios
        movimientos_lista = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)] # U, D, L, R, Diagonales por fila y columna

        for casilla in self.estados_posibles:
            fila, columna = self.casilla_a_coordenadas(casilla)

            for fila_mov_list, colum_mov_list in movimientos_lista:
                nueva_fila, nueva_columna = fila + fila_mov_list, columna + colum_mov_list

                if (0 <= nueva_fila < self.filas) and 0 <= (nueva_columna < self.columnas):
                    nueva_casilla = self.coordenada_a_casilla(nueva_fila, nueva_columna)
                    transiciones_posibles[casilla].add(nueva_casilla)

        return transiciones_posibles

class Jugador:
    def __init__(self, numero, cadena):
        self.numero = numero
        self.cadena = cadena
    

class Juego:
    def __init__(self, tablero, jugador):
        self.tablero = tablero
        self.jugador = jugador

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