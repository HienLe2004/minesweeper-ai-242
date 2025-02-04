from setting import *
import pygame_gui
from cell import *
from grid import *
from blindSearch import BFS_Search
from heuristicSearch import Heuristic_Search 
import time
import tracemalloc

class Game:
    def __init__(self, row, col):
        self.ROW = row
        self.COL = col
        self.CELL_SIZE = min(MAX_MAIN_SCREEN_HEIGHT//row, MAX_MAIN_SCREEN_WIDTH//col)
        self.SCREEN_WIDTH_OFFSET = 300
        self.MAIN_SCREEN_WIDTH = self.CELL_SIZE * col + self.SCREEN_WIDTH_OFFSET
        self.MAIN_SCREEN_HEIGH = self.CELL_SIZE * row
        self.running = True
        self.is_solved = False
        pygame.init()
        self.screen = pygame.display.set_mode((self.MAIN_SCREEN_WIDTH, self.MAIN_SCREEN_HEIGH))
        pygame.display.set_caption('MineSweeper')
        self.clock = pygame.time.Clock()
        self.grid = Grid(self.screen, (self.ROW, self.COL), 
                         (self.CELL_SIZE, self.CELL_SIZE), 10,
                         (self.MAIN_SCREEN_WIDTH/2 - self.SCREEN_WIDTH_OFFSET/2, self.MAIN_SCREEN_HEIGH/2))
        self.manager = pygame_gui.UIManager((self.MAIN_SCREEN_WIDTH, self.MAIN_SCREEN_HEIGH))
        self.manager.get_theme().load_theme('themes/game_theme.json')
        bfs_btn_surf = pygame.Surface((200,50))
        bfs_btn_rect = bfs_btn_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 10))
        self.bfs_button = pygame_gui.elements.UIButton(relative_rect=bfs_btn_rect, text="BFS", 
                                                       manager=self.manager,
                                                       object_id="#bfs_btn")
        heuristic_btn_surf = pygame.Surface((200,50))
        heuristic_btn_rect = heuristic_btn_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 60))
        self.heuristic_button = pygame_gui.elements.UIButton(relative_rect=heuristic_btn_rect, text="Heuristic", 
                                                       manager=self.manager,
                                                       object_id="#heuristic_btn")
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            self.manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.bfs_button:
                    self.is_solved = False
                    print("Solving by BFS algorithm...")
                    print("Input grid:")
                    grid_data = self.grid.get_grid_data()
                    for row in grid_data:
                        print(row)
                    if self.grid.first_solve:
                        self.grid.first_solve = False
                        self.grid.original_grid_data = grid_data
                    else:
                        grid_data = self.grid.original_grid_data
                    start_time = time.time()  # Lấy thời gian bắt đầu
                    tracemalloc.start() # Bắt đầu theo dõi
                    result = BFS_Search(grid_data)
                    self.grid.set_grid_data(result)
                    # computer_result = solve_minesweeper(challenge_board)
                    current, peak = tracemalloc.get_traced_memory() # Lấy thông tin bộ nhớ
                    end_time = time.time()  # Lấy thời gian kết thúc
                    execution_time = end_time - start_time  # Thời gian thực thi
                    self.is_solved = True
                    self.execution_time = execution_time
                    self.current_capacity = current
                    self.peak_capacity = peak
                    print("Output grid:")
                    for row in result:
                        print(row)
                elif event.ui_element == self.heuristic_button:
                    self.is_solved = False
                    print("Solving by Heuristic algorithm...")
                    print("Input grid:")
                    grid_data = self.grid.get_grid_data()
                    for row in grid_data:
                        print(row)
                    if self.grid.first_solve:
                        self.grid.first_solve = False
                        self.grid.original_grid_data = grid_data
                    else:
                        grid_data = self.grid.original_grid_data
                    start_time = time.time()  # Lấy thời gian bắt đầu
                    tracemalloc.start() # Bắt đầu theo dõi
                    result = Heuristic_Search(grid_data, self.grid)
                    self.grid.set_grid_data(result)
                    # computer_result = solve_minesweeper(challenge_board)
                    current, peak = tracemalloc.get_traced_memory() # Lấy thông tin bộ nhớ
                    end_time = time.time()  # Lấy thời gian kết thúc
                    execution_time = end_time - start_time  # Thời gian thực thi
                    self.is_solved = True
                    self.execution_time = execution_time
                    self.current_capacity = current
                    self.peak_capacity = peak
                    print("Output grid:")
                    for row in result:
                        print(row)

    def draw(self):
        self.screen.fill((0,0,0))
        self.grid.draw()
        if self.is_solved:
            self.show_result()

    def show_result(self):
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        text_1 = font.render(f"Execution time: {self.execution_time:.4f} s", True, (250,250,250))
        text_2 = font.render(f"Current cap: {self.current_capacity / 1024:.2f} KB", True, (250,250,250))
        text_3 = font.render(f"Peak cap: {self.peak_capacity / 1024:.2f} KB", True, (250,250,250))
        text_rect_1 = text_1.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 120))
        text_rect_2 = text_2.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 150))
        text_rect_3 = text_3.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 180))
        self.screen.blit(text_1, text_rect_1)
        self.screen.blit(text_2, text_rect_2)
        self.screen.blit(text_3, text_rect_3)

    def update(self):
        self.input()
        self.grid.update()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.update()
            self.draw()
            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
        pygame.quit()
