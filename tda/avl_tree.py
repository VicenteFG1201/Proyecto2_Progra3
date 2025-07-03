class AVLNode:
    def __init__(self, path):
        self.path = path  # Camino "A → B → C"
        self.frequency = 1  # Inicialmente usado una vez
        self.height = 1
        self.left = None
        self.right = None

def get_height(node):
    return node.height if node else 0

def get_balance(node):
    return get_height(node.left) - get_height(node.right) if node else 0

def rotate_right(y):
    x = y.left
    T = x.right
    x.right = y
    y.left = T
    y.height = max(get_height(y.left), get_height(y.right)) + 1
    x.height = max(get_height(x.left), get_height(x.right)) + 1
    return x

def rotate_left(x):
    y = x.right
    T = y.left
    y.left = x
    x.right = T
    x.height = max(get_height(x.left), get_height(x.right)) + 1
    y.height = max(get_height(y.left), get_height(y.right)) + 1
    return y

def insert_route(root, path):
    if not root:
        return AVLNode(path)
    
    if path < root.path:
        root.left = insert_route(root.left, path)
    elif path > root.path:
        root.right = insert_route(root.right, path)
    else:
        root.frequency += 1
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    balance = get_balance(root)

    if balance > 1 and path < root.left.path:
        return rotate_right(root)
    if balance < -1 and path > root.right.path:
        return rotate_left(root)
    if balance > 1 and path > root.left.path:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if balance < -1 and path < root.right.path:
        root.right = rotate_right(root.right)
        return rotate_left(root)

    return root
