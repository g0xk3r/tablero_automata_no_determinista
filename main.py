import random
import sys
import pygame
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
    def __init__(self, id_jugador, estado_inicial, estado_final):
        self.id = id_jugador
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.posicion_actual = estado_inicial
        self.ruta_asignada = []
        self.rutas_ganadoras = []
        self.rutas_perdedoras = []

    def creacion_rutas(self, num_movimientos, tablero):
        self.rutas_ganadoras.clear()
        self.rutas_perdedoras.clear()
        punto_partida = [self.estado_inicial]
        self.buscar_rutas(punto_partida, num_movimientos, tablero)
        self.archivar_rutas_ganadoras('ganadoras')
        self.archivar_rutas_perdedoras('perdedoras')
        print(f"Archivos generados de jugador {self.id}")

    def buscar_rutas(self, ruta_actual, num_max_movimientos, tablero):
        if len(ruta_actual) - 1 == num_max_movimientos:
            estado_final_ruta = ruta_actual[-1]
            if estado_final_ruta == self.estado_final:
                self.rutas_ganadoras.append(list(ruta_actual))
            else:
                self.rutas_perdedoras.append(list(ruta_actual))
            return
        estado_actual = ruta_actual[-1]
        posibles_siguientes_estados = tablero.transiciones.get(estado_actual, set())
        for siguiente_estado in posibles_siguientes_estados:
            nueva_ruta = list(ruta_actual)
            nueva_ruta.append(siguiente_estado)
            self.buscar_rutas(ruta_actual + [siguiente_estado], num_max_movimientos, tablero)

    def guardar_rutas_archivo(self, tipo_ruta):
        if tipo_ruta == 'ganadoras':
            listas_rutas = self.rutas_ganadoras
            nombre_archivo = f'jugador_{self.id}_rutas_ganadoras.txt'
        else:
            listas_rutas = self.rutas_perdedoras
            nombre_archivo = f'jugador_{self.id}_rutas_perdedoras.txt'

        with open(nombre_archivo, 'w') as archivo:
            if not listas_rutas:
                archivo.write("No hay rutas disponibles.\n")
                return
            for ruta in listas_rutas:
                archivo.write(', '.join(map(str, ruta)) + '\n')

class Juego:
    def __init__(self, tablero, jugadores):
        pygame.init()
        # Atributos del juego
        self.tablero = tablero
        self.jugadores = jugadores
        self.ganador = None
        self.casillas_ocupadas = {j.posicion_actual for j in self.jugador}

        # Configuracion grafica
        self.tam_casilla = 100
        self.margen = 5
        ancho = (self.tablero.columnas * self.tam_casilla) + (2 * self.margen)
        self.pantalla = pygame.display.set_mode((ancho, ancho))
        pygame.display.set_caption("Tablero de Juego")
        self.color_blanco = (255, 255, 255)
        self.color_negro = (0, 0, 0)
        self.color_gris = (200, 200, 200)
        self.colores_jugador = {
            1: (255, 0, 0),
            2: (0, 255, 0),
            3: (0, 0, 255)
        }

    def asignar_rutas_aleatorias(self):
        for jugador in self.jugadores:
            if jugador.rutas_ganadoras:
                jugador.ruta_asignada = random.choice(jugador.rutas_ganadoras)
                print(f"Jugador {jugador.id} ha sido asignado la ruta ganadora: {jugador.ruta_asignada}")
            else:
                jugador.ruta_asignada = []
                print(f"Jugador {jugador.id} no tiene rutas ganadoras disponibles.")

    def mostrar_tablero(self):
        for fila in range(self.tablero.filas):
            for columna in range(self.tablero.columnas):
                casilla = pygame.Rect(
                    self.margen + (columna * self.tam_casilla),
                    self.margen + (fila * self.tam_casilla),
                    self.tam_casilla,
                    self.tam_casilla
                )
                pygame.draw.rect(self.pantalla, self.color_negro, casilla, 2)

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