from fastapi import APIRouter
from dashboard import st  # O usa un singleton/global para acceder a los datos

router = APIRouter()

@router.get("/")
def list_clients():
    return [client.to_dict() for client in st.session_state.clients.values()]

@router.get("/{client_id}")
def get_client(client_id: str):
    for client in st.session_state.clients.values():
        if client.client_id == client_id:
            return client.to_dict()
    return {"error": "Cliente no encontrado"}
