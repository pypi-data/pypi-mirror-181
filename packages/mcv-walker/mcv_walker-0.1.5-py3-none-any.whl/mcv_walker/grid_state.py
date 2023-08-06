import numpy as np


class GridState:
    def __init__(self, player_x: int, player_y: int, explored_grid: np.ndarray):
        self.player_x: int = player_x
        self.player_y: int = player_y
        self.explored_grid: np.ndarray = explored_grid
        self.explored_count: int = 0
