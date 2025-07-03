class Client:
    def __init__(self, client_id, nombre, tipo):
        self.client_id = client_id
        self.nombre = nombre
        self.tipo = tipo
        self.total_orders = 0  # Inicializa el contador

    def add_order(self):
        self.total_orders += 1

    def to_dict(self):
        return {
            "client_id": self.client_id,
            "nombre": self.nombre,
            "tipo": self.tipo,
            "total_orders": self.total_orders
        }
