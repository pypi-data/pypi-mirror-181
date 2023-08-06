class LayerLevelSize:
    def __init__(self, z: int, size: float, layers: dict[str, int]):
        self.z = z
        self.size = size
        self.layers = layers


class TileItemSize:
    def __init__(self, x: int, y: int, z: int, size: float, layers: dict[str, int]):
        self.x = x
        self.y = y
        self.z = z
        self.size = size
        self.layers = layers
