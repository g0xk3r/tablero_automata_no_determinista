import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def graficar_rutas_jugador(jugador, num_movimientos):
    ruta_ganadoras = jugador.carpeta / f'jugador_{jugador.id}_rutas_ganadoras.txt'
    ruta_perdedoras = jugador.carpeta / f'jugador_{jugador.id}_rutas_perdedoras.txt'
    G = nx.DiGraph()
    todos_nodos = set()
    todas_aristas = set()

    def procesar_archivo(ruta_archivo):
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                linea_limpia = linea.strip()
                if not linea_limpia or linea_limpia == "No hay rutas disponibles.":
                    continue
                ruta = [int(estado.strip()) for estado in linea_limpia.split(',')]
                for t in range(len(ruta)):
                    nodo = (t, ruta[t])
                    todos_nodos.add(nodo)
                    if t > 0:
                        nodo_anterior = (t - 1, ruta[t-1])
                        todas_aristas.add((nodo_anterior, nodo))

    procesar_archivo(ruta_ganadoras)
    procesar_archivo(ruta_perdedoras)
    if not todos_nodos:
        print(f"No hay rutas para graficar para el jugador {jugador.id}.")
        return
    G.add_nodes_from(todos_nodos)
    G.add_edges_from(todas_aristas)
    pos = {nodo: (nodo[0], nodo[1]) for nodo in G.nodes()}
    nodo_inicial = (0, jugador.estado_inicial)
    nodos_finales_ganadores = {n for n in todos_nodos if n[0] == num_movimientos and n[1] == jugador.estado_final}
    nodos_finales_perdedores = {n for n in todos_nodos if n[0] == num_movimientos and n[1] != jugador.estado_final}
    nodos_intermedios = todos_nodos - {nodo_inicial} - nodos_finales_ganadores - nodos_finales_perdedores
    plt.figure(figsize=(18, 10))
    nx.draw_networkx_nodes(G, pos, nodelist=[nodo_inicial], node_color='lime', node_size=300)
    nx.draw_networkx_nodes(G, pos, nodelist=nodos_finales_ganadores, node_color='red', node_size=300)
    nx.draw_networkx_nodes(G, pos, nodelist=nodos_finales_perdedores, node_color='#cccccc', node_size=300) # Gris
    nx.draw_networkx_nodes(G, pos, nodelist=nodos_intermedios, node_color='skyblue', node_size=300)
    nx.draw_networkx_edges(G, pos, alpha=0.1, arrows=True, arrowstyle='->')
    labels = {nodo: nodo[1] for nodo in G.nodes()} # Etiqueta es el estado (casilla)
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='black')

    plt.title(f"NFA de Jugador {jugador.id} (Ei: {jugador.estado_inicial}, Ef: {jugador.estado_final})", fontsize=16)
    plt.xlabel("Cadena", fontsize=12)
    plt.ylabel("Estado (Casilla)", fontsize=12)
    plt.xticks(range(num_movimientos + 1))
    plt.yticks(range(1, 17))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()