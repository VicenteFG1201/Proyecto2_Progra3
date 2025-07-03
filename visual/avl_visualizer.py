import networkx as nx
import matplotlib.pyplot as plt

def build_graph_from_avl(node, G=None, parent=None):
    if G is None:
        G = nx.DiGraph()
    if node:
        label = f"{node.path}\nFreq: {node.frequency}"
        G.add_node(label)

        if parent:
            G.add_edge(parent, label)

        build_graph_from_avl(node.left, G, label)
        build_graph_from_avl(node.right, G, label)

    return G

def draw_avl_tree(avl_root):
    G = build_graph_from_avl(avl_root)
    pos = hierarchy_pos(G)

    fig, ax = plt.subplots(figsize=(12, 6))
    nx.draw(G, pos, with_labels=True, node_color="lightgreen", node_size=1500, font_size=10, ax=ax)
    return fig

# Posición jerárquica para AVL
def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    import networkx as nx
    pos = {}

    def _hierarchy_pos(G, root, leftmost, width, vert_gap, vert_loc, xcenter, pos, parent=None):
        neighbors = list(G.neighbors(root))
        if len(neighbors) != 2:
            width /= 2
        pos[root] = (xcenter, vert_loc)
        if neighbors:
            if len(neighbors) >= 1:
                left, *rest = neighbors
                pos = _hierarchy_pos(G, left, leftmost, width, vert_gap, vert_loc - vert_gap, xcenter - width / 2, pos, root)
            if len(neighbors) == 2:
                right = neighbors[1]
                pos = _hierarchy_pos(G, right, leftmost, width, vert_gap, vert_loc - vert_gap, xcenter + width / 2, pos, root)
        return pos

    if root is None:
        root = list(nx.topological_sort(G))[0]
    return _hierarchy_pos(G, root, 0, width, vert_gap, vert_loc, xcenter, pos)
