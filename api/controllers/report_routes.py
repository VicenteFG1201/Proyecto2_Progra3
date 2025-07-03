from fastapi import APIRouter
from fastapi.responses import FileResponse
from visual.report_generator import generate_pdf
from dashboard import st  # O usa un singleton/global para acceder a los datos

router = APIRouter()

@router.get("/pdf")
def download_pdf():
    # Genera el PDF con los datos actuales
    filename = generate_pdf(
        st.session_state.clients,
        st.session_state.orders,
        st.session_state.avl_root,
        filename="informe_drones.pdf"
    )
    return FileResponse(filename, media_type='application/pdf', filename="informe_drones.pdf")
