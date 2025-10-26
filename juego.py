import random
import sys
import pygame
from pathlib import Path

class Juego:
    def __init__(self, tablero, jugadores, num_movimientos):
        pygame.init()
        # Atributos del juego
        self.tablero = tablero
        self.jugadores = jugadores
        self.ganador = None
        self.casillas_ocupadas = {j.posicion_actual for j in self.jugadores}
        self.movimientos_totales = num_movimientos
        self.indices_reconfig = {1: [], 2: [], 3: []}

        # Configuracion grafica
        self.tam_casilla = 100
        self.margen = 5
        ancho = (self.tablero.columnas * self.tam_casilla) + (2 * self.margen)
        self.pantalla = pygame.display.set_mode((ancho, ancho))
        pygame.display.set_caption("Tablero de Juego")
        self.texto_fuente = pygame.font.SysFont(None, 50)
        self.color_blanco = (255, 255, 255)
        self.color_casilla_negro = (0, 0, 0)
        self.color_casilla_rojo = (255, 0, 0)
        self.colores_jugador = {
            1: (255, 0, 0),
            2: (0, 255, 0),
            3: (0, 0, 255)
        }
        self.fuente_ruta = pygame.font.SysFont(None, 30)
        self.colores_segmentos = [
            (0, 0, 0), # Negro
            (255, 0, 0), # Rojo
            (0, 0, 255), # Azul
            (0, 150, 0), # Verde
            (150, 0, 150), # Morado
            (255, 128, 0) # Naranja
        ]

    def asignar_rutas_aleatorias(self):
        for jugador in self.jugadores:
            num_rutas = jugador.conteo_ganadas
            ruta_random = None
            if num_rutas > 0:
                indice_linea_rand = random.randint(0, num_rutas - 1)
                indice_linea_actual = 0
                carpeta = jugador.carpeta
                ruta_archivo_buscado = carpeta / f"jugador_{jugador.id}_rutas_ganadoras.txt"
                with open(ruta_archivo_buscado, 'r', encoding="utf-8") as archivo:
                    for linea in archivo:
                        if indice_linea_actual == indice_linea_rand:
                            linea_sin_espacios = linea.strip()
                            if linea_sin_espacios and linea_sin_espacios != "No hay rutas disponibles.":
                                ruta_random = [int(estado.strip()) for estado in linea_sin_espacios.split(',')]
                            break
                        indice_linea_actual += 1
            if ruta_random:
                jugador.ruta_asignada = ruta_random
                print(f"Ruta asignada al jugador {jugador.id}: {jugador.ruta_asignada}")
            else:
                jugador.ruta_asignada = []
                print(f"No se asigno ruta al jugador {jugador.id} porque no tiene rutas ganadoras.")

    def mostrar_tablero(self):
        for fila in range(self.tablero.filas):
            for columna in range(self.tablero.columnas):
                num_casilla = self.tablero.coordenada_a_casilla(fila, columna)
                color_casilla = self.tablero.color_casilla(num_casilla)
                if color_casilla == 'b':
                    pintar_color = self.color_casilla_negro
                else:
                    pintar_color = self.color_casilla_rojo
                casilla = pygame.Rect(
                    self.margen + (columna * self.tam_casilla),
                    self.margen + (fila * self.tam_casilla),
                    self.tam_casilla,
                    self.tam_casilla
                )
                pygame.draw.rect(self.pantalla, pintar_color, casilla)

    def mostrar_piezas(self):
        for jugador in self.jugadores:
            fila, columna = self.tablero.casilla_a_coordenadas(jugador.posicion_actual)
            xcentro = self.margen + columna * self.tam_casilla + self.tam_casilla // 2
            ycentro = self.margen + fila * self.tam_casilla + self.tam_casilla // 2
            radio = self.tam_casilla // 3
            pygame.draw.circle(
                self.pantalla,
                self.colores_jugador[jugador.id],
                (xcentro, ycentro),
                radio
            )
            pygame.draw.circle(
                self.pantalla,
                self.color_blanco,
                (xcentro, ycentro),
                radio,
                3
            )
            numero_texto = str(jugador.id)
            texto_superficie = self.texto_fuente.render(numero_texto, True, self.color_blanco)
            texto = texto_superficie.get_rect()
            texto.center = (xcentro, ycentro)
            self.pantalla.blit(texto_superficie, texto)

    def reconfigurar_ruta(self, jugador_actual, rutas_falladas_turno):
        indice_actual = jugador_actual.movimiento_actual
        casilla_actual = jugador_actual.posicion_actual
        ruta_archivo = jugador_actual.carpeta / f"jugador_{jugador_actual.id}_rutas_ganadoras.txt"
        nueva_ruta_encontrada = None
        indice_objetivo = indice_actual + 1

        with open(ruta_archivo, 'r', encoding="utf-8") as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                if not linea_limpia or linea_limpia == "No hay rutas disponibles.":
                    continue
                ruta_candidata = [int(estado.strip()) for estado in linea_limpia.split(',')]
                if ruta_candidata in rutas_falladas_turno:
                    continue
                if not (len(ruta_candidata) > indice_objetivo) and (ruta_candidata[indice_actual] == casilla_actual): # Mismo punto actual
                    nueva_ruta_encontrada = ruta_candidata
                    continue
                siguiente_paso = ruta_candidata[indice_objetivo]
                if siguiente_paso not in self.casillas_ocupadas:
                    nueva_ruta_encontrada = ruta_candidata
                    break

        if nueva_ruta_encontrada:
            jugador_actual.ruta_asignada = nueva_ruta_encontrada
            print(f"Ruta reconfigurada: {jugador_actual.ruta_asignada}")
            return True
        else:
            print(f"No se encontro ruta para reconfigurar.")
            return False

    def mostrar_pantalla_final(self):
        self.pantalla = pygame.display.set_mode((1200,500))
        self.pantalla.fill(self.color_blanco)
        titulo_surf = self.texto_fuente.render("Recorridos Finales", True, self.color_casilla_negro)
        titulo_rect = titulo_surf.get_rect(center=(self.pantalla.get_width() // 2, 40))
        self.pantalla.blit(titulo_surf, titulo_rect)
        y_pos = 100 # Posición Y inicial

        for jugador in self.jugadores:
            x_pos = 20 # Resetea X
            texto_jugador = f"Jugador {jugador.id}: ["
            surf_titulo = self.fuente_ruta.render(texto_jugador, True, self.color_casilla_negro)
            self.pantalla.blit(surf_titulo, (x_pos, y_pos))
            x_pos += surf_titulo.get_width()
            ruta_final = jugador.ruta_asignada

            if not ruta_final:
                surf = self.fuente_ruta.render("No se asigno ruta.]", True, self.color_casilla_negro)
                self.pantalla.blit(surf, (x_pos, y_pos))
                y_pos += 40
                continue

            puntos_de_corte = sorted(list(set([0] + self.indices_reconfig[jugador.id] + [len(ruta_final)])))
            color_index = 0
            for i in range(len(puntos_de_corte) - 1):
                idx_inicio = puntos_de_corte[i]
                idx_fin = puntos_de_corte[i+1]
                if idx_inicio >= idx_fin:
                    continue

                segmento_lista = ruta_final[idx_inicio:idx_fin]
                segmento_str = ", ".join(map(str, segmento_lista))
                if idx_fin != len(ruta_final):
                    segmento_str += ", "

                color = self.colores_segmentos[color_index % len(self.colores_segmentos)]
                surf = self.fuente_ruta.render(segmento_str, True, color)
                self.pantalla.blit(surf, (x_pos, y_pos))
                x_pos += surf.get_width()
                color_index += 1

            surf_final = self.fuente_ruta.render("]", True, self.color_casilla_negro)
            self.pantalla.blit(surf_final, (x_pos, y_pos))
            y_pos += 40 # Siguiente línea

        pygame.display.flip()
        espera_final = True
        while espera_final:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT or evento.type == pygame.KEYDOWN:
                    espera_final = False

    def iniciar_partida(self):
        random.shuffle(self.jugadores)
        print("El orden de las jugadas será:")
        for i, jugador in enumerate(self.jugadores):
            print(f"{i+1} - jugador {jugador.id}")

        self.pantalla.fill(self.color_blanco)
        self.mostrar_tablero()
        self.mostrar_piezas()
        pygame.display.flip()

        indice_turno_jugador = 0
        corriendo = True
        ronda = 1
        tiempo_inicio = pygame.time.get_ticks()
        esperando = True

        while esperando: # Espera 2 segundos antes de iniciar
            if pygame.time.get_ticks() - tiempo_inicio > 2000:
                esperando = False
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    esperando = False
                    corriendo = False

        while corriendo:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    corriendo = False
            if not self.ganador:
                jugador_actual = self.jugadores[indice_turno_jugador]
                rutas_falladas_turno = []
                intentando_mover = True
                while intentando_mover:
                    if not jugador_actual.ruta_asignada: # Comprobar ruta vacia
                        print(f"Jugador {jugador_actual.id} no tiene ruta. Pierde turno.")
                        intentando_mover = False
                    elif jugador_actual.movimiento_actual >= self.movimientos_totales:
                        pass # Si ya termino salta turno
                        intentando_mover = False
                    else:
                        indice_sig_casilla = jugador_actual.movimiento_actual + 1
                        sig_casilla_objetivo = jugador_actual.ruta_asignada[indice_sig_casilla]
                        print(f"Jugador {jugador_actual.id} (mov {indice_sig_casilla}/{self.movimientos_totales}) intenta ir a {sig_casilla_objetivo}")
                        if sig_casilla_objetivo in self.casillas_ocupadas:
                            print(f"Casilla {sig_casilla_objetivo} ocupada. Reconfigurando ruta...")
                            # No se incrementa su contador, lo intentará de nuevo
                            rutas_falladas_turno.append(list(jugador_actual.ruta_asignada))
                            reconfiguracion_exitosa = self.reconfigurar_ruta(jugador_actual, rutas_falladas_turno)
                            if reconfiguracion_exitosa:
                                print("Intentando de nuevo...")
                                self.indices_reconfig[jugador_actual.id].append(jugador_actual.movimiento_actual + 1)
                            else:
                                print("Pierde el turno.")
                                intentando_mover = False
                        else:
                            print("Hecho")
                            self.casillas_ocupadas.remove(jugador_actual.posicion_actual)
                            jugador_actual.posicion_actual = sig_casilla_objetivo
                            self.casillas_ocupadas.add(jugador_actual.posicion_actual)
                            jugador_actual.movimiento_actual += 1
                            intentando_mover = False
                            if (jugador_actual.movimiento_actual == self.movimientos_totales) and (jugador_actual.posicion_actual == jugador_actual.estado_final):
                                self.ganador = jugador_actual
                                print(f"Ganador de la partida: Jugador {jugador_actual.id}")

                if not self.ganador:
                    todos_terminaron = all(jug.movimiento_actual >= self.movimientos_totales for jug in self.jugadores)
                    if todos_terminaron:
                        print("Todos los jugadores terminaron sus movimientos pero no hay ganador.")
                        corriendo = False
                    if corriendo:
                        indice_turno_jugador += 1
                        if indice_turno_jugador >= len(self.jugadores):
                            indice_turno_jugador = 0
                            print(f"Fin de ronda {ronda}\n")
                            ronda += 1

            if corriendo and not self.ganador:
                pygame.time.wait(1000)

            self.pantalla.fill(self.color_blanco)
            self.mostrar_tablero()
            self.mostrar_piezas()
            pygame.display.flip()
        print("Fin de juego.")
        self.mostrar_pantalla_final()
        pygame.quit()
        sys.exit()