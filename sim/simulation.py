from route_management import generate_graph, bfs_route_with_recharge
from sim.order_generator import generate_clients, generate_orders
from tda.avl_tree import insert_route

def run_simulation(n_nodes, m_edges, max_energy, n_orders):
    graph = generate_graph(n_nodes, m_edges)
    charging_nodes = [n for n, data in graph.nodes(data=True) if data['role'] == 'recarga']
    clients = generate_clients(graph, n_clients=30)
    avl_root = None

    orders, avl_root = generate_orders(
        graph,
        clients,
        max_energy,
        charging_nodes,
        bfs_route_with_recharge, 
        avl_root,
        n_orders
    )

    return graph, clients, orders, avl_root, charging_nodes
