import networkx as nx
import random
import streamlit as st
import matplotlib.pyplot as plt

def generate_graph(n_nodes, m_edges):
    # Garantizar conectividad y el número correcto de aristas
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))
    # Primero, crear un árbol para asegurar conectividad
    nodes = list(G.nodes())
    random.shuffle(nodes)
    for i in range(1, n_nodes):
        weight = random.randint(1, 10)
        G.add_edge(nodes[i - 1], nodes[i], weight=weight)
    # Luego, agregar aristas aleatorias hasta alcanzar m_edges
    edges_added = n_nodes - 1
    while edges_added < m_edges:
        u, v = random.sample(nodes, 2)
        if not G.has_edge(u, v):
            weight = random.randint(1, 10)
            G.add_edge(u, v, weight=weight)
            edges_added += 1
    for node in G.nodes():
        # Coordenadas aleatorias en Temuco
        lat = random.uniform(-38.77, -38.70)
        lon = random.uniform(-72.65, -72.55)
        G.nodes[node]['coords'] = (lat, lon)
    assign_roles(G)
    return G


def bfs_route_with_recharge(graph, start, goal, max_energy, charging_nodes):
    """
    Busca una ruta desde start hasta goal respetando el límite de batería.
    Usa BFS y fuerza paso por nodos de recarga si la energía no alcanza.
    """
    if start not in graph or goal not in graph:
        return [], 0

    queue = [(start, [start], 0, max_energy)]  # (nodo, camino, costo acumulado, energía restante)
    visited = set()

    while queue:
        node, path, cost, energy_left = queue.pop(0)
        if node == goal:
            return path, cost

        visited.add((node, energy_left))
        for neighbor in graph.neighbors(node):
            edge_cost = graph[node][neighbor].get('weight', 1)
            new_energy = energy_left - edge_cost
            # Si el nodo vecino es de recarga, recarga la batería
            if neighbor in charging_nodes:
                new_energy = max_energy
            if new_energy >= 0 and (neighbor, new_energy) not in visited:
                queue.append((neighbor, path + [neighbor], cost + edge_cost, new_energy))

    return [], 0  # No hay ruta posible

def assign_roles(graph):
    """
    Asigna roles a cada nodo del grafo:
    - 20% almacenamiento
    - 20% recarga
    - 60% cliente
    """
    n = graph.number_of_nodes()
    nodes = list(graph.nodes())
    random.shuffle(nodes)

    n_storage = int(0.2 * n)
    n_recharge = int(0.2 * n)
    n_clients = n - n_storage - n_recharge

    for i, node in enumerate(nodes):
        if i < n_storage:
            graph.nodes[node]['role'] = 'almacenamiento'
        elif i < n_storage + n_recharge:
            graph.nodes[node]['role'] = 'recarga'
        else:
            graph.nodes[node]['role'] = 'cliente'

def dijkstra_route(graph, start, goal):
    try:
        path = nx.dijkstra_path(graph, start, goal, weight='weight')
        cost = nx.dijkstra_path_length(graph, start, goal, weight='weight')
        return path, cost
    except nx.NetworkXNoPath:
        return None, float('inf')

def floyd_warshall_all_pairs(graph):
    return dict(nx.floyd_warshall(graph, weight='weight'))

def minimum_spanning_tree(graph):
    return nx.minimum_spanning_tree(graph, algorithm="kruskal")

# Elimina o mueve el ejemplo bajo este condicional:
if __name__ == "__main__":
    G = generate_graph(15, 20)
    charging_nodes = set([2, 6, 10])  # Ejemplo de nodos de recarga
    origin, destination, max_energy = 0, 13, 50  # Ejemplo de origen, destino y energía máxima
    algoritmo = st.selectbox("Algoritmo de ruta", ["BFS", "Dijkstra"])
    if st.button("Calcular ruta"):
        if algoritmo == "BFS":
            path, cost = bfs_route_with_recharge(G, origin, destination, max_energy, charging_nodes)
        else:
            path, cost = dijkstra_route(G, origin, destination)
    with st.tabs("Árbol de Expansión Mínima (Kruskal)"):
        st.header("Árbol de Expansión Mínima (Kruskal)")
        if st.session_state.get("running"):
            mst = minimum_spanning_tree(st.session_state.graph)
            pos = nx.spring_layout(mst)
            fig, ax = plt.subplots(figsize=(10, 6))
            nx.draw(mst, pos, with_labels=True, node_color="lightblue", edge_color="red", ax=ax)
            st.pyplot(fig)
