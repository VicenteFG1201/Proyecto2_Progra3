def summarize_flight(graph, path):
    if not path or len(path) < 2:
        return {
            "Distancia total": "0 unidades",
            "Consumo estimado": "0%",
            "Tiempo estimado": "0 min"
        }
    distancia_total = 0
    for i in range(len(path) - 1):
        u, v = path[i], path[i+1]
        distancia_total += graph[u][v].get('weight', 1)
    bateria = min(50, distancia_total)
    tiempo_est = distancia_total / 10.0
    return {
        "Distancia total": f"{distancia_total} unidades",
        "Consumo estimado": f"{bateria}%",
        "Tiempo estimado": f"{tiempo_est:.1f} min"
    }
