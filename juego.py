import random
import sys
import pygame

class Juego:
    def __init__(self, tablero, jugadores):
        pygame.init()
        # Atributos del juego
        self.tablero = tablero
        self.jugadores = jugadores
        self.ganador = None
        self.casillas_ocupadas = {j.posicion_actual for j in self.jugadores}

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
                indice_turno_jugador += 1
                if indice_turno_jugador >= len(self.jugadores):
                    indice_turno_jugador = 0
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