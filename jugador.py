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
        self.guardar_rutas_archivo('ganadoras')
        self.guardar_rutas_archivo('perdedoras')
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