from fastapi import APIRouter
from dashboard import st  # Acceso a los datos reales

router = APIRouter()

@router.get("/visits/clients")
def ranking_clientes():
    if not st.session_state.running:
        return []
    G = st.session_state.graph
    orders = st.session_state.orders
    client_visits = {}
    for order in orders:
        dest = order.destination
        if G.nodes[dest]['role'] == 'cliente':
            client_visits[dest] = client_visits.get(dest, 0) + 1
    # Devuelve lista ordenada por visitas
    return [{"client_id": k, "visitas": v} for k, v in sorted(client_visits.items(), key=lambda x: -x[1])]

@router.get("/visits/recharges")
def ranking_recargas():
    if not st.session_state.running:
        return []
    G = st.session_state.graph
    orders = st.session_state.orders
    recharge_visits = {}
    for order in orders:
        if hasattr(order, "path"):
            for node in order.path:
                if G.nodes[node]['role'] == 'recarga':
                    recharge_visits[node] = recharge_visits.get(node, 0) + 1
    return [{"node_id": k, "visitas": v} for k, v in sorted(recharge_visits.items(), key=lambda x: -x[1])]

@router.get("/visits/storages")
def ranking_almacenamiento():
    if not st.session_state.running:
        return []
    G = st.session_state.graph
    orders = st.session_state.orders
    storage_visits = {}
    for order in orders:
        if hasattr(order, "path"):
            for node in order.path:
                if G.nodes[node]['role'] == 'almacenamiento':
                    storage_visits[node] = storage_visits.get(node, 0) + 1
    return [{"node_id": k, "visitas": v} for k, v in sorted(storage_visits.items(), key=lambda x: -x[1])]

@router.get("/summary")
def resumen_global():
    if not st.session_state.running:
        return {}
    G = st.session_state.graph
    orders = st.session_state.orders
    unique_clients = set()
    total_battery = 0
    total_routes = 0
    for order in orders:
        unique_clients.add(order.destination)
        if hasattr(order, "path") and order.path:
            total_battery += len(order.path)
            total_routes += 1
    avg_battery = (total_battery / total_routes) if total_routes else 0
    return {
        "total_ordenes": len(orders),
        "clientes_únicos": len(unique_clients),
        "rutas_registradas": total_routes,
        "uso_batería_promedio": avg_battery
    }
