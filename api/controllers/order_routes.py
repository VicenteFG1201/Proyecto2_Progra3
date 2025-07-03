from fastapi import APIRouter
from dashboard import st  # O usa un singleton/global para acceder a los datos

router = APIRouter()

@router.get("/")
def list_orders():
    return [order.to_dict() for order in st.session_state.orders]

@router.get("/orders/{order_id}")
def get_order(order_id: str):
    for order in st.session_state.orders:
        if order.id == order_id:
            return order.to_dict()
    return {"error": "Orden no encontrada"}

@router.post("/orders/{order_id}/cancel")
def cancel_order(order_id: str):
    for order in st.session_state.orders:
        if order.id == order_id and order.status not in ["cancelled", "completed"]:
            order.status = "cancelled"
            return {"status": "Orden cancelada"}
    return {"error": "No se puede cancelar esta orden"}

@router.post("/orders/{order_id}/complete")
def complete_order(order_id: str):
    for order in st.session_state.orders:
        if order.id == order_id and order.status != "completed":
            order.status = "completed"
            return {"status": "Orden completada"}
    return {"error": "No se puede completar esta orden"}
