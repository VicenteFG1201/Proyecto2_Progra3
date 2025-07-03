import random
from domain.client import Client
from domain.order import Order
from tda.avl_tree import insert_route
from tda.hash_map import HashMap

def generate_clients(graph, n_clients):
    clients = HashMap()
    client_nodes = [n for n, data in graph.nodes(data=True) if data['role'] == 'cliente']
    random.shuffle(client_nodes)

    for i in range(min(n_clients, len(client_nodes))):
        client_id = f"C{i}"
        name = f"Cliente {i}"
        tipo = "cliente"
        clients.set(client_nodes[i], Client(client_id, name, tipo))

    return clients

def generate_orders(graph, clients, max_energy, charging_nodes, bfs_func, avl_root, n_orders):
    orders = []
    order_id = 1
    almacen_nodes = [n for n, data in graph.nodes(data=True) if data['role'] == 'almacenamiento']

    # Extraer todas las claves de clientes del HashMap
    client_nodes = []
    for bucket in clients.table:
        for key, _ in bucket:
            client_nodes.append(key)

    for _ in range(n_orders):
        origin = random.choice(almacen_nodes)
        destination = random.choice(client_nodes)

        path, cost = bfs_func(graph, origin, destination, max_energy, charging_nodes)
        if path:
            client = clients.get(destination)
            order = Order(origin, destination, path)
            order.client_id = client.client_id
            order.cost = cost
            client.add_order()
            orders.append(order)

            # Insertar ruta al AVL
            path_str = " → ".join(map(str, path))
            avl_root = insert_route(avl_root, path_str)

            order_id += 1

    return orders, avl_root
