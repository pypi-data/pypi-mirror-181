import copy
import os
from typing import List

import numpy as np
from rich import print

from mcv_walker.direction import Direction
from mcv_walker.grid_state import GridState


class GridWalker:
    def __init__(self):
        self.width: int = 15
        self.height: int = 15
        self.portal_symbol = '&'
        self.player_symbol = '@'
        self.explored_overflow_symbol = '.'
        self.unexplored_symbol = '#'
        self.grid_state: GridState = self.new_grid_state()
        self.grid_state_history: List[GridState] = []

    def new_grid_state(self):
        player_x: int = self.width // 2
        player_y: int = self.height // 2
        explored_grid: np.ndarray = np.full([self.height, self.width], fill_value=self.unexplored_symbol)
        explored_grid[player_y, player_x] = self.portal_symbol
        grid_state = GridState(player_x, player_y, explored_grid)
        return grid_state

    def print_grid(self):
        display_string = ''
        for row_index, row in enumerate(self.grid_state.explored_grid):
            for column_index, cell in enumerate(row):
                background_color = 'grey'
                foreground_color = 'black'
                character = cell
                if character == self.portal_symbol:
                    background_color = 'purple'
                elif character == '1':
                    background_color = 'red'
                elif character != self.unexplored_symbol:
                    background_color = 'green'
                if row_index == self.grid_state.player_y and column_index == self.grid_state.player_x:
                    foreground_color = 'orange_red1'
                    character = self.player_symbol
                cell_display_string = f'[{foreground_color} on {background_color}]{character}[/]'
                display_string += cell_display_string
            display_string += '\n'
        os.system('cls' if os.name == 'nt' else 'clear')
        print(display_string)

    def move_and_print(self, direction: Direction):
        self.append_grid_state_history(self.grid_state)
        if direction == Direction.UP:
            self.grid_state.player_y -= 1
        elif direction == Direction.DOWN:
            self.grid_state.player_y += 1
        elif direction == Direction.RIGHT:
            self.grid_state.player_x += 1
        elif direction == Direction.LEFT:
            self.grid_state.player_x -= 1
        if self.grid_state.explored_grid[self.grid_state.player_y, self.grid_state.player_x] == self.unexplored_symbol:
            self.grid_state.explored_count += 1
            if self.grid_state.explored_count < 10:
                self.grid_state.explored_grid[self.grid_state.player_y, self.grid_state.player_x] = \
                    str(self.grid_state.explored_count)
            else:
                self.grid_state.explored_grid[self.grid_state.player_y, self.grid_state.player_x] = \
                    self.explored_overflow_symbol
        self.print_grid()

    def append_grid_state_history(self, grid_state: GridState):
        self.grid_state_history.append(copy.deepcopy(grid_state))
        if len(self.grid_state_history) > 10:
            self.grid_state_history.pop(0)

    def undo(self):
        if len(self.grid_state_history) != 0:
            self.grid_state = self.grid_state_history.pop()
            self.print_grid()

    def reset(self):
        self.append_grid_state_history(self.grid_state)
        self.grid_state = self.new_grid_state()
        self.print_grid()
