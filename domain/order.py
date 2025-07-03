import uuid

class Order:
    def __init__(self, origin_id, dest_id, route):
        self.id = str(uuid.uuid4())[:8]
        self.origin = origin_id
        self.destination = dest_id
        self.route = route
        self.status = "pending"
        self.created_at = "2025-06-30"
        self.priority = "normal"
        self.delivery_date = None
        self.total_cost = len(route) * 10  # Por ejemplo

    def to_dict(self):
        return {
            "id": self.id,
            "origin": self.origin,
            "destination": self.destination,
            "route": self.route,
            "status": self.status,
            "created_at": self.created_at,
            "priority": self.priority,
            "delivery_date": self.delivery_date,
            "total_cost": self.total_cost
        }
