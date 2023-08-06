import os

import numpy as np
from rich import print

from mcv_walker.direction import Direction


class GridWalker:
    def __init__(self):
        self.width: int = 15
        self.height: int = 15
        self.player_x: int = self.width // 2
        self.player_y: int = self.height // 2
        self.portal_symbol = '&'
        self.player_symbol = '@'
        self.explored_overflow_symbol = '.'
        self.unexplored_symbol = '#'
        self.explored_count = 0
        self.explored_grid: np.ndarray = np.full([self.height, self.width], fill_value=self.unexplored_symbol)
        self.explored_grid[self.player_y, self.player_x] = self.portal_symbol

    def print_grid(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for row_index, row in enumerate(self.explored_grid):
            for column_index, cell in enumerate(row):
                background_color = 'grey'
                foreground_color = 'black'
                character = cell
                if row_index == self.player_y and column_index == self.player_x:
                    foreground_color = 'orange_red1'
                    character = self.player_symbol
                if character == self.portal_symbol:
                    background_color = 'purple'
                elif character == '1':
                    background_color = 'red'
                elif character != self.unexplored_symbol:
                    background_color = 'green'
                cell_display_string = f'[{foreground_color} on {background_color}]{character}[/]'
                print(cell_display_string, end='')
            print('')

    def move_and_print(self, direction: Direction):
        if direction == Direction.UP:
            self.player_y -= 1
        elif direction == Direction.DOWN:
            self.player_y += 1
        elif direction == Direction.RIGHT:
            self.player_x += 1
        elif direction == Direction.LEFT:
            self.player_x -= 1
        if self.explored_grid[self.player_y, self.player_x] == self.unexplored_symbol:
            self.explored_count += 1
            if self.explored_count < 10:
                self.explored_grid[self.player_y, self.player_x] = str(self.explored_count)
            else:
                self.explored_grid[self.player_y, self.player_x] = self.explored_overflow_symbol
        self.print_grid()
