import folium

def build_map(graph, mst=None):
    m = folium.Map(location=[-38.7359, -72.5904], zoom_start=13)  
    for n, data in graph.nodes(data=True):
        color = {"almacenamiento": "blue", "recarga": "green", "cliente": "orange"}.get(data["role"], "gray")
        folium.CircleMarker(location=data["coords"], radius=6, color=color, fill=True).add_to(m)
    for u, v in graph.edges():
        folium.PolyLine([graph.nodes[u]["coords"], graph.nodes[v]["coords"]], color="gray").add_to(m)
    if mst is not None:
        for u, v in mst.edges():
            folium.PolyLine(
                [graph.nodes[u]["coords"], graph.nodes[v]["coords"]],
                color="red",
                weight=4,
                dash_array="10"
            ).add_to(m)
    return m._repr_html_()