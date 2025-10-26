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

                if (0 <= nueva_fila < self.filas) and (0 <= nueva_columna < self.columnas):
                    nueva_casilla = self.coordenada_a_casilla(nueva_fila, nueva_columna)
                    transiciones_posibles[casilla].add(nueva_casilla)

        return transiciones_posibles

    def color_casilla(self, casilla):
        fila, columna = self.casilla_a_coordenadas(casilla)
        if (fila + columna) % 2 == 0:
            return 'b'
        else:
            return 'r'