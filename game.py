from setting import *
import setting
import pygame_gui
from cell import *
from grid import *
from checkbox import *
from blindSearch import BFS_Search, DFS_Search
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
        input_rect_surf = pygame.Surface((100,50))
        input_rect = input_rect_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 110))
        self.grid_input = pygame_gui.elements.UITextEntryLine(relative_rect=input_rect,
                                                             manager=self.manager, object_id="#grid_input",
                                                             initial_text='[]')
        input_btn_surf = pygame.Surface((100,50))
        input_btn_rect = input_btn_surf.get_rect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 110, 110))
        self.input_button = pygame_gui.elements.UIButton(relative_rect=input_btn_rect, text="input", 
                                                       manager=self.manager,
                                                       object_id="#input_btn")
        self.checkbox = Checkbox(self.screen, (self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 20, 180), (20,20))

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
                    # if self.grid.first_solve:
                    #     self.grid.first_solve = False
                    #     self.grid.original_grid_data = grid_data
                    # else:
                    #     grid_data = self.grid.original_grid_data
                    start_time = time.time()  # Lấy thời gian bắt đầu
                    tracemalloc.start() # Bắt đầu theo dõi
                    # result = DFS_Search(grid_data)
                    result = BFS_Search(grid_data,self)
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
                    # if self.grid.first_solve:
                    #     self.grid.first_solve = False
                    #     self.grid.original_grid_data = grid_data
                    # else:
                    #     grid_data = self.grid.original_grid_data
                    start_time = time.time()  # Lấy thời gian bắt đầu
                    tracemalloc.start() # Bắt đầu theo dõi
                    if self.checkbox.is_checked:
                        result = Heuristic_Search(grid_data, self)
                    else:
                        result = Heuristic_Search(grid_data)
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
                elif event.ui_element == self.input_button:
                    self.is_solved = False
                    if self.grid_input.get_text() in ['','[]']:
                        res = [[-1] * self.COL] * self.ROW
                        self.grid.set_grid_data(res)
                        return
                    res = []
                    rows = self.grid_input.get_text().split(',')
                    for r in rows:
                        int_cells = []
                        for c in r:
                            if c == '-':
                                int_cells.append(-1)
                            else:
                                int_cells.append(int(c))
                        res.append(int_cells)
                    print(res)
                    self.grid.set_grid_data(res)
                    setting.current_state = 0
                    
    def draw(self):
        self.screen.fill((0,0,0))
        self.grid.draw()
        if self.is_solved:
            self.show_result()
        self.checkbox.draw()
        #show current state
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        text = font.render(f"State #{setting.current_state}", True, (250,250,250))
        text_rect = text.get_frect(bottomleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 700))
        self.screen.blit(text, text_rect)

    def draw_every_states(self):

        self.screen.fill((0,0,0))
        self.grid.draw()
        if self.is_solved:
            self.show_result()
        #show current state
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        text = font.render(f"State #{setting.current_state}", True, (250,250,250))
        text_rect = text.get_frect(bottomleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 700))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        # time.sleep(1)

    def show_result(self):
        font = pygame.font.Font('fonts/Electrolize-Regular.ttf', 16)
        text_1 = font.render(f"Execution time: {self.execution_time:.4f} s", True, (250,250,250))
        text_2 = font.render(f"Current cap: {self.current_capacity / 1024:.2f} KB", True, (250,250,250))
        text_3 = font.render(f"Peak cap: {self.peak_capacity / 1024:.2f} KB", True, (250,250,250))
        text_rect_1 = text_1.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 200))
        text_rect_2 = text_2.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 230))
        text_rect_3 = text_3.get_frect(topleft=(self.MAIN_SCREEN_WIDTH - self.SCREEN_WIDTH_OFFSET + 10, 260))
        self.screen.blit(text_1, text_rect_1)
        self.screen.blit(text_2, text_rect_2)
        self.screen.blit(text_3, text_rect_3)

    def update(self):
        self.input()
        self.grid.update()
        self.checkbox.update()

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.update()
            self.draw()
            self.manager.update(dt)
            self.manager.draw_ui(self.screen)
            pygame.display.update()
        pygame.quit()
