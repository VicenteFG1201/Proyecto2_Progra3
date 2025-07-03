from visual.avl_visualizer import draw_avl_tree
import streamlit as st 
import networkx as nx
import matplotlib.pyplot as plt
from route_management import generate_graph, bfs_route_with_recharge, dijkstra_route, floyd_warshall_all_pairs
from sim.simulation import run_simulation  
import random  
from collections import Counter
from visual.maps_builder import build_map
from visual.flight_summary import summarize_flight

# Configuración inicial
st.set_page_config(page_title="Simulación de Drones", layout="wide")
st.title("Sistema de Drones Autónomos VFA")

# Estado global
if "graph" not in st.session_state:
    st.session_state.graph = None
if "charging_nodes" not in st.session_state:
    st.session_state.charging_nodes = []
if "running" not in st.session_state:
    st.session_state.running = False

# Pestañas
tabs = st.tabs([
    "Run Simulation",
    "Explore Network",
    "Clients & Orders",
    "Route Analytics",
    "General Statistics"
])


# Pestaña 1: Correr Simulación

with tabs[0]:
    st.header("Configurar Simulación")

    n_nodes = st.slider("Número de nodos", 10, 150, 15)
    m_edges = st.slider("Número de aristas", n_nodes-1, n_nodes*2, 25)
    n_orders = st.slider("Número de órdenes (simulado)", 1, 300, 10)
    max_energy = st.slider("Autonomía del dron (energía máx)", 10, 100, 50)

    if st.button("Iniciar Simulación"):
        G, clients, orders, avl_root, charging_nodes = run_simulation(n_nodes, m_edges, max_energy, n_orders)
        st.session_state.graph = G
        st.session_state.clients = clients
        st.session_state.orders = orders
        st.session_state.avl_root = avl_root
        st.session_state.charging_nodes = charging_nodes
        st.session_state.running = True
        st.success("Simulación completada con éxito.")

    if st.button("Reiniciar"):
        st.session_state.running = False
        st.session_state.graph = None


# Pestaña 2: Explorar

with tabs[1]:
    st.header("Explorar Red de Drones")

    if not st.session_state.running:
        st.warning("Primero debes iniciar la simulación en la pestaña anterior.")
    else:
        G = st.session_state.graph
        charging_nodes = st.session_state.charging_nodes
        max_energy = 50  # Puedes adaptar este valor al slider si lo deseas

        nodes = list(G.nodes())
        client_nodes = [n for n in nodes if G.nodes[n].get("role") == "cliente"]

        col1, col2 = st.columns(2)
        with col1:
            origin = st.selectbox("Nodo origen (almacenamiento)", [n for n in nodes if G.nodes[n].get("role") == "almacenamiento"])
        with col2:
            destination = st.selectbox("Nodo destino (cliente)", client_nodes)

        algoritmo = st.radio("Algoritmo de ruta", ["BFS", "Dijkstra", "Floyd-Warshall"])
        if st.button("Calcular ruta"):
            if algoritmo == "BFS":
                path, cost = bfs_route_with_recharge(G, origin, destination, max_energy, charging_nodes)
            elif algoritmo == "Dijkstra":
                path, cost = dijkstra_route(G, origin, destination)
            else:  # Floyd-Warshall
                dist_matrix = floyd_warshall_all_pairs(G)
                try:
                    path = nx.reconstruct_path(origin, destination, dist_matrix)
                    cost = dist_matrix[origin][destination]
                except Exception:
                    path, cost = [], float('inf')

            if path and len(path) > 1:
                resumen = summarize_flight(G, path)
                st.info(
                    f"**Resumen de vuelo:**\n"
                    f"- Distancia total: {resumen['Distancia total']}\n"
                    f"- Consumo estimado: {resumen['Consumo estimado']}\n"
                    f"- Tiempo estimado: {resumen['Tiempo estimado']}"
                )
                st.success(f"Ruta encontrada: {' → '.join(map(str, path))} | Costo: {cost}")

                # Botón para completar entrega y crear orden
                if st.button("✅ Complete Delivery and Create Order"):
                    from domain.order import Order
                    import uuid
                    order_id = str(uuid.uuid4())[:8]
                    new_order = Order(origin, destination, path)
                    new_order.status = "completed"
                    if "orders" not in st.session_state:
                        st.session_state.orders = []
                    st.session_state.orders.append(new_order)
                    st.success(f"Orden {order_id} creada y completada.")
                # Dibujar la ruta
                pos = nx.spring_layout(G, seed=42)
                edge_colors = []
                for u, v in G.edges():
                    if any((u == path[i] and v == path[i+1]) or (u == path[i+1] and v == path[i])
                           for i in range(len(path) - 1)):
                        edge_colors.append("red")
                    else:
                        edge_colors.append("gray")

                node_colors = []
                for n in G.nodes():
                    role = G.nodes[n].get("role", "")
                    if role == "almacenamiento":
                        node_colors.append("blue")
                    elif role == "recarga":
                        node_colors.append("green")
                    elif role == "cliente":
                        node_colors.append("orange")
                    else:
                        node_colors.append("gray")

                fig, ax = plt.subplots(figsize=(10, 6))
                nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors,
                        node_size=500, font_size=10, ax=ax)
                st.pyplot(fig)
            else:
                st.error("No se encontró una ruta válida con la batería actual o los nodos seleccionados.")
        
        # Mostrar el mapa interactivo
        from route_management import minimum_spanning_tree

        if st.button("🌲 Show MST (Kruskal)"):
            mst = minimum_spanning_tree(G)
            st.components.v1.html(build_map(G, mst=mst), height=600)
        else:
            st.components.v1.html(build_map(G), height=600)

# Pestaña 3: Clientes & Ordenes

with tabs[2]:
    st.header("Clientes y Órdenes")

    if not st.session_state.running:
        st.warning("Primero debes iniciar la simulación en la pestaña 1.")
    else:
        st.subheader("Clientes Activos")
        for bucket in st.session_state.clients.table:
            for nodo_id, client in bucket:
                st.json({
                    "Nodo ID": nodo_id,
                    "ID Cliente": client.client_id,
                    "Nombre": client.nombre,
                    "Total de pedidos": client.total_orders
                })

        st.subheader("Órdenes Generadas")
        for order in st.session_state.orders:
            st.json({
                "ID Orden": order.id,
                "Cliente": getattr(order, "client_id", ""),
                "Origen": order.origin,
                "Destino": order.destination,
                "Costo": getattr(order, "cost", ""),
                "Prioridad": getattr(order, "priority", ""),
                "Estado": order.status
            })

# 📋 Pestaña 4: Análisis de Ruta

with tabs[3]:
    st.header("Rutas más frecuentes (AVL Tree)")

    if not st.session_state.running:
        st.warning("Primero debes ejecutar la simulación.")
    else:
        avl_root = st.session_state.avl_root
        if avl_root is None:
            st.info("No se han registrado rutas aún.")
        else:
            fig = draw_avl_tree(avl_root)
            st.pyplot(fig)

    from visual.report_generator import generate_pdf

    if st.button("📄 Generar Informe PDF"):
        filename = generate_pdf(
            st.session_state.clients,
            st.session_state.orders,
            st.session_state.avl_root,
            filename="informe_drones.pdf"
        )
        with open(filename, "rb") as f:
            st.download_button(
                label="Descargar Informe PDF",
                data=f,
                file_name="informe_drones.pdf",
                mime="application/pdf"
            )

# 📈 Pestaña 5: Estadísticas Generales

with tabs[4]:
    st.header("Estadísticas Generales del Sistema")

    if not st.session_state.running:
        st.warning("Primero debes ejecutar la simulación.")
    else:
        G = st.session_state.graph
        orders = st.session_state.orders

        # Contar visitas a nodos por tipo (usamos como destino)
        visit_counter = Counter()
        for order in orders:
            if hasattr(order, "path") and order.path:
                for node in order.path:
                    role = G.nodes[node]['role']
                    visit_counter[role] += 1
            else:
                # Fallback: solo el destino
                role = G.nodes[order.destination]['role']
                visit_counter[role] += 1

        # Contar cantidad total de nodos por tipo
        role_distribution = Counter()
        for _, data in G.nodes(data=True):
            role_distribution[data['role']] += 1

        # Gráfico de barras: nodos más visitados
        st.subheader("Nodos más visitados por tipo (como destino)")

        roles = ["cliente", "recarga", "almacenamiento"]
        colores = {"cliente": "orange", "recarga": "green", "almacenamiento": "blue"}
        valores = [visit_counter.get(rol, 0) for rol in roles]
        colores_barras = [colores[rol] for rol in roles]

        fig1, ax1 = plt.subplots()
        ax1.bar(roles, valores, color=colores_barras)
        ax1.set_ylabel("Cantidad de visitas")
        st.pyplot(fig1)

        # Gráfico de torta: proporción de nodos por rol
        st.subheader(" Proporción de nodos por tipo")
        fig2, ax2 = plt.subplots()
        ax2.pie(role_distribution.values(), labels=role_distribution.keys(), autopct='%1.1f%%', startangle=90)
        ax2.axis("equal")
        st.pyplot(fig2)