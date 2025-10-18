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

    def mostrar_piezas(self):
        for jugador in self.jugadores:
            fila, columna = self.tablero.casilla_a_coordenadas(jugador.posicion_actual)
            xcentro = self.margen + columna * self.tam_casilla + self.tam_casilla // 2
            ycentro = self.margen + fila * self.tam_casilla + self.tam_casilla // 2
            pygame.draw.circle(
                self.pantalla,
                self.colores_jugador[jugador.id],
                (xcentro, ycentro),
                self.tam_casilla // 3 # radio de circulo
            )

    def iniciar_partida(self):
        random.shuffle(self.jugadores)
        print("El orden de las jugadas será:")
        for i, jugador in enumerate(self.jugadores):
            print(f"{i+1} - jugador {jugador.id}")
        turno_mov = 0
        indice_turno_jugador = 0
        if self.jugadores[0].ruta_asignada:
            num_movimientos_total = len(self.jugadores[0].ruta_asignada) - 1
        else:
            num_movimientos_total = 0
        corriendo = True

        while corriendo:
            # Hasta aqui revisar
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False

            if turno_mov < num_movimientos_total and not self.ganador:
                jugador_actual = self.jugadores[indice_turno_jugador]
                sig_casilla_objetivo = jugador_actual.ruta_asignada[turno_mov + 1]
                print(f"Jugador {jugador_actual.id} se mueve a la casilla {sig_casilla_objetivo}")

                if sig_casilla_objetivo in self.casillas_ocupadas:
                    print(f"Casilla {sig_casilla_objetivo} ocupada. Jugador {jugador_actual.id} pierde su turno.") # modificar para calcular el resto del nuevo vector
                else:
                    self.casillas_ocupadas.remove(jugador_actual.posicion_actual)
                    jugador_actual.posicion_actual = sig_casilla_objetivo
                    self.casillas_ocupadas.add(jugador_actual.posicion_actual)

                    if jugador_actual.posicion_actual == jugador_actual.estado_final:
                        self.ganador = jugador_actual
                        print(f"¡El jugador {jugador_actual.id} ha ganado la partida!")
                turno_jugador += 1
                if indice_turno_jugador >= len(self.jugadores):
                    turno_jugador = 0
                    turno_mov += 1
                    print(f"Fin de ronda {turno_mov}.")

                pygame.time.wait(1000)
            self.pantalla.fill(self.color_blanco)
            self.mostrar_tablero()
            self.mostrar_piezas()
            pygame.display.flip()
        print("Fin del juego.")
        if self.ganador:
            print(f"El ganador es el jugador {self.ganador.id}")
        else:
            print("No hay ganador.")
        pygame.quit()
        sys.exit()

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

if __name__ == "__main__":
    option = menu()
    if option != 0:
        long_cadena = pedir_tam_cadena(option)
        cadenas = [pedir_cadena(long_cadena, option) for _ in range(3)]
        print("Cadenas ingresadas:", cadenas)
        tablero = Tablero(4, 4)
        jugadores = [
            Jugador(1, 1, 16),
            Jugador(2, 4, 13),
            Jugador(3, 3, 14)
        ]
        num_movimientos = long_cadena
        for jugador in jugadores:
            jugador.creacion_rutas(num_movimientos, tablero)

        juego_visual = Juego(tablero, jugadores)
        juego_visual.asignar_rutas_aleatorias()
        juego_visual.iniciar_partida()
    else:
        print("Programa terminado.")