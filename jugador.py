from pathlib import Path
class Jugador:
    def __init__(self, id_jugador, estado_inicial, estado_final):
        self.id = id_jugador
        self.estado_inicial = estado_inicial
        self.estado_final = estado_final
        self.posicion_actual = estado_inicial
        self.ruta_asignada = []
        self.movimiento_actual = 0
        self.conteo_ganadas = 0
        self.conteo_perdedoras = 0
        self.carpeta = Path("archivos_rutas")

    def creacion_rutas(self, num_movimientos, tablero, cadena):
        self.conteo_ganadas = 0
        self.conteo_perdedoras = 0
        self.carpeta.mkdir(exist_ok=True)
        rutas_ganadoras = self.carpeta / f'jugador_{self.id}_rutas_ganadoras.txt'
        rutas_perdedoras = self.carpeta / f'jugador_{self.id}_rutas_perdedoras.txt'
        punto_partida = [self.estado_inicial]

        with open(rutas_ganadoras, 'w', encoding='utf-8') as archivo_ganadoras, open(rutas_perdedoras, 'w', encoding='utf-8') as archivo_perdedoras:
            self.buscar_rutas(punto_partida, num_movimientos, tablero, archivo_ganadoras, archivo_perdedoras, cadena)

        if self.conteo_ganadas == 0:
            self.no_rutas(rutas_ganadoras)
        if self.conteo_perdedoras == 0:
            self.no_rutas(rutas_perdedoras)

    def buscar_rutas(self, ruta_actual, num_max_movimientos, tablero, archivo_ganadoras, archivo_perdedoras, cadena):
        if len(ruta_actual) - 1 == num_max_movimientos:
            estado_final_ruta = ruta_actual[-1]
            escribir_ruta = ', '.join(map(str, ruta_actual)) + '\n'

            if estado_final_ruta == self.estado_final:
                archivo_ganadoras.write(escribir_ruta)
                self.conteo_ganadas += 1
            else:
                archivo_perdedoras.write(escribir_ruta)
                self.conteo_perdedoras += 1
            return
        estado_actual = ruta_actual[-1]
        posibles_siguientes_estados = tablero.transiciones.get(estado_actual, set())
        indice_mov_actual = len(ruta_actual) - 1
        color_requerido = cadena[indice_mov_actual]
        for sig_estado in posibles_siguientes_estados:
            color_respectivo = tablero.color_casilla(sig_estado)
            if color_respectivo == color_requerido:
                self.buscar_rutas(
                    ruta_actual + [sig_estado],
                    num_max_movimientos,
                    tablero,
                    archivo_ganadoras,
                    archivo_perdedoras,
                    cadena
                )

    def no_rutas(self, ruta_archivo):
        with open(ruta_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write("No hay rutas disponibles.\n")