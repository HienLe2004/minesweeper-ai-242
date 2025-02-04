from setting import *
from enum import Enum
class Cell_Type(Enum):
    MINE = -2
    HIDE = -1
    EMPTY = -3
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8

class Cell:
    color_mapping = {
        0: (200, 200, 200),
        1: (0, 0, 200),
        2: (0, 100, 0),
        3: (200, 0, 0),
        4: (0, 0, 100),
        5: (100, 0, 0),
        6: (0, 100, 100),
        7: (100, 100, 0),
        8: (80, 80, 80)
    }
    light_color = (200, 200, 200)
    medium_color = (150, 150, 150)
    medium_dark_color = (100, 100, 100)
    dark_color = (50, 50, 50)
    exploded_color = (250, 0, 0)
    flag = pygame.image.load('image/red-flag.png')
    mine = pygame.image.load('image/mine.png')
    def __init__(self, grid, grid_position=(0, 0), size=(50, 50), type=Cell_Type.EMPTY):
        self.size = size
        Cell.flag = pygame.transform.scale(Cell.flag, self.size)
        Cell.flag = pygame.transform.scale_by(Cell.flag, 0.75)
        Cell.mine = pygame.transform.scale(Cell.mine, self.size)
        self.grid = grid
        self.grid_position = grid_position
        self.position = ((self.grid_position[1] + 0.5)*self.size[0], (self.grid_position[0] + 0.5)*self.size[1])
        self.type = type
        self.cell_surf = pygame.Surface(self.size)
        self.cell_rect = self.cell_surf.get_frect(center=self.position)
        self.is_hovered = False

    def input(self):
        mouse_pos = pygame.mouse.get_pos()
        modified_mouse_pos = (mouse_pos[0] - self.grid.grid_rect.left, mouse_pos[1] - self.grid.grid_rect.top)
        mouse_buttons = pygame.mouse.get_just_released()
        self.is_hovered = self.cell_rect.collidepoint(modified_mouse_pos)
        if self.is_hovered:
            if mouse_buttons[0]:
                self.grid.change_cell(self.grid_position, True)
            elif mouse_buttons[2]:
                self.grid.change_cell(self.grid_position, False)

    def draw(self):
        if self.type.value >= 0:
            pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.medium_color, rect=self.cell_rect)
            pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.medium_dark_color, rect=self.cell_rect, width=1)
            font = pygame.font.Font('freesansbold.ttf', int(self.size[0]*0.8))
            text = font.render(str(self.type.value), True, Cell.color_mapping[self.type.value])
            text_rect = text.get_frect(center=self.position).move(0, int(self.size[0]*0.08))
            self.grid.grid_surf.blit(text, text_rect)
        elif self.type == Cell_Type.EMPTY:
            pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.medium_color, rect=self.cell_rect)
            pygame.draw.rect(surface=self.grid.grid_surf, color=Cell.medium_dark_color, rect=self.cell_rect, width=1)
        else:
            #non-flag
            pygame.draw.polygon(surface=self.grid.grid_surf, color=Cell.light_color, points=[self.cell_rect.topleft, self.cell_rect.topright, self.cell_rect.bottomleft])
            pygame.draw.polygon(surface=self.grid.grid_surf, color=Cell.dark_color, points=[self.cell_rect.topright, self.cell_rect.bottomright, self.cell_rect.bottomleft])
            if self.is_hovered:
                pygame.draw.rect(surface=self.grid.grid_surf, color=self.light_color, rect=self.cell_rect.scale_by(0.8))
            else:
                pygame.draw.rect(surface=self.grid.grid_surf, color=self.medium_color, rect=self.cell_rect.scale_by(0.8))
            #flagged
            if self.type.value == -2:
                flag_rect = Cell.flag.get_frect(center=self.position)
                self.grid.grid_surf.blit(Cell.flag, flag_rect)
            
    
    def update(self):
        self.input()