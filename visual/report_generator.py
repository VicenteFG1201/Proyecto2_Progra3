from fpdf import FPDF
import os

def generate_pdf(clients, orders, avl_root, filename="reporte.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(0, 10, "Reporte de Simulación de Drones", ln=True, align="C")
    pdf.ln(10)

    # Tabla de clientes
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Clientes", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.cell(40, 8, "ID", 1)
    pdf.cell(60, 8, "Nombre", 1)
    pdf.cell(40, 8, "Total Pedidos", 1)
    pdf.ln()
    for bucket in clients.table:
        for nodo_id, client in bucket:
            pdf.cell(40, 8, safe_str(client.client_id), 1)
            pdf.cell(60, 8, safe_str(client.nombre), 1)
            pdf.cell(40, 8, safe_str(client.total_orders), 1)
            pdf.ln()
    pdf.ln(5)

    # Tabla de órdenes
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Órdenes", ln=True)
    pdf.set_font("Arial", size=8)
    headers = ["ID", "Cliente", "Origen", "Destino", "Costo", "Prioridad", "Estado"]
    for h in headers:
        pdf.cell(25, 8, h, 1)
    pdf.ln()
    for order in orders:
        pdf.cell(25, 8, safe_str(order.id), 1)
        pdf.cell(25, 8, safe_str(getattr(order, "client_id", "")), 1)
        pdf.cell(25, 8, safe_str(order.origin), 1)
        pdf.cell(25, 8, safe_str(order.destination), 1)
        pdf.cell(25, 8, safe_str(getattr(order, "cost", "")), 1)
        pdf.cell(25, 8, safe_str(getattr(order, "priority", "")), 1)
        pdf.cell(25, 8, safe_str(order.status), 1)
        pdf.ln()
    pdf.ln(5)

    # Rutas frecuentes (AVL)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Rutas más frecuentes (AVL)", ln=True)
    pdf.set_font("Arial", size=10)
    def in_order(node):
        if node:
            in_order(node.left)
            pdf.cell(0, 8, safe_str(f"{node.path} | Frecuencia: {node.frequency}"), ln=True)
            in_order(node.right)
    if avl_root:
        in_order(avl_root)
    else:
        pdf.cell(0, 8, "No hay rutas registradas.", ln=True)

    # Guarda el PDF en la carpeta actual
    pdf.output(filename)
    return os.path.abspath(filename)

def safe_str(s):
    return str(s).encode("latin1", "replace").decode("latin1")