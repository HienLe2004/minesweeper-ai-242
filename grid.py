import random
from setting import *
from cell import *

class Grid:
    def __init__(self, screen, grid_size=(10, 10), cell_size=(50, 50), number_of_mines=30, position=(300, 300)):
        self.screen = screen
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.grid_surf = pygame.Surface((grid_size[1] * cell_size[0], grid_size[0] * cell_size[1]))
        self.position = position
        self.grid_rect = self.grid_surf.get_frect(center=self.position) 
        self.number_of_mines = number_of_mines
        self.cells = []
        self.is_generated_mines = False
        self.first_solve = True
        self.original_grid_data = None
        for row in range(grid_size[0]):
            cells_in_row = []
            for col in range(grid_size[1]):
                cells_in_row.append(Cell(self, (row,col), self.cell_size, Cell_Type.HIDE))
            self.cells.append(cells_in_row)

    def change_cell(self, grid_position, forward):
        # print(f'Change cell at {grid_position}')
        cell = self.cells[grid_position[0]][grid_position[1]]
        if forward:
            if cell.type == Cell_Type.EIGHT:
                cell.type = Cell_Type.HIDE
            elif cell.type == Cell_Type.EMPTY:
                cell.type = Cell_Type.ZERO
            elif cell.type == Cell_Type.HIDE:
                cell.type = Cell_Type.EMPTY
            else:
                cell.type = Cell_Type(cell.type.value + 1)
            return
        if cell.type == Cell_Type.HIDE:
            cell.type = Cell_Type.EIGHT
        elif cell.type == Cell_Type.ZERO:
            cell.type = Cell_Type.EMPTY
        elif cell.type == Cell_Type.EMPTY:
            cell.type = Cell_Type.HIDE
        else:
            cell.type = Cell_Type(cell.type.value - 1)

    def set_grid_data(self, data):
        for row in range(self.grid_size[0]):
            for col in range(self.grid_size[1]):
                self.cells[row][col].type = Cell_Type(data[row][col])

    def get_grid_data(self):
        return [[cell.type.value for cell in row] for row in self.cells]

    def draw(self):
        self.grid_surf.fill((120, 120, 0))
        for row in self.cells:
            for cell in row:
                cell.draw()
        self.screen.blit(self.grid_surf, self.grid_rect)

    def update(self):
        for row in self.cells:
            for cell in row:
                cell.update()