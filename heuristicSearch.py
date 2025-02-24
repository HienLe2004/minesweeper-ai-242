import math
from itertools import combinations
from cell import Cell_Type
import time
import setting

delay_time = 1

# challenge_board=[[h,h,h,1,h],
#                  [h,3,4,h,2],
#                  [h,h,h,4,h],
#                  [h,h,h,4,h],
#                  [h,2,3,h,h]]

# challenge_board=[[h,h,0,h,h,1,h],
#                  [h,2,h,h,h,h,h],
#                  [2,h,h,2,3,h,h],
#                  [1,h,2,h,3,2,h],
#                  [1,h,2,h,4,h,h],
#                  [h,h,h,h,h,h,2],
#                  [h,1,h,2,3,h,h]]

# challenge_board=[[h,h,h,2,h,2,h,h,h,1],
#                  [h,3,h,h,h,h,1,1,2,h],
#                  [h,3,h,h,3,h,h,h,h,h],
#                  [0,h,1,2,h,h,h,2,3,h],
#                  [h,h,1,h,1,2,h,h,2,h],
#                  [1,h,h,3,h,2,1,h,h,h],
#                  [2,h,h,h,h,h,h,h,h,3],
#                  [h,4,h,h,3,h,1,h,h,h],
#                  [2,h,h,2,h,h,h,h,3,3],
#                  [h,h,1,1,2,2,h,h,1,h]]

# challenge_board=[[2,h,h,h,2,h,h,h,2,h,0,h,h,3,h,4,h,h,h,h],
#                  [h,2,h,1,2,h,h,2,h,h,h,1,h,h,h,h,h,5,3,1],
#                  [h,1,h,h,h,1,h,2,h,2,h,h,h,h,h,3,h,h,h,2],
#                  [h,1,h,h,h,h,3,h,h,h,h,h,h,h,1,h,3,h,h,3],
#                  [h,1,h,2,h,2,h,h,h,h,2,h,1,1,h,1,h,h,h,h],
#                  [h,h,1,1,h,2,h,4,h,3,h,1,2,3,3,h,h,2,2,h],
#                  [h,h,h,h,1,1,h,3,h,h,h,h,h,h,h,h,3,h,4,2],
#                  [h,3,3,h,h,1,1,h,3,h,h,2,h,h,h,h,h,h,h,h],
#                  [h,h,h,h,3,h,2,h,3,h,1,h,1,3,h,h,3,4,h,4],
#                  [h,2,3,h,h,h,h,1,h,h,3,h,h,3,h,h,1,h,h,h],
#                  [h,h,h,h,h,h,h,h,h,h,h,h,h,h,h,3,h,h,4,h],
#                  [h,h,0,h,1,h,h,h,h,3,5,h,h,1,h,h,h,h,h,1],
#                  [0,h,h,h,2,h,1,h,h,h,3,h,h,h,1,1,1,h,h,1],
#                  [h,h,h,h,3,h,2,h,1,2,h,h,2,h,2,h,1,h,h,1],
#                  [h,4,h,3,2,h,h,h,h,h,h,h,h,h,h,h,h,h,h,h],
#                  [2,h,h,h,1,h,h,1,h,h,h,h,h,h,2,3,h,2,h,3],
#                  [h,h,2,h,h,0,h,1,h,1,h,2,h,h,2,h,h,1,h,h],
#                  [h,1,1,h,1,0,h,h,h,h,3,h,3,h,h,h,h,2,h,h],
#                  [2,h,h,1,2,h,h,h,2,h,h,2,h,h,2,h,1,h,2,h],
#                  [h,h,1,h,h,h,h,1,h,3,h,2,h,h,h,h,h,h,1,h]]

def check_valid_board(board):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if(0 <= board[row][col] <= 8):
                bomb_neighbor = 0
                unOpened = 0
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == Cell_Type.MINE.value:
                        bomb_neighbor += 1
                    elif 0 <= nr < size and 0 <= nc < size and board[nr][nc] == Cell_Type.HIDE.value:
                        unOpened += 1

                if(board[row][col] < bomb_neighbor or (unOpened + bomb_neighbor) < board[row][col]): return False
    return True

def check_goal_board(board):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if(board[row][col] != Cell_Type.HIDE.value and board[row][col] != Cell_Type.MINE.value and board[row][col] != Cell_Type.EMPTY.value):
                bomb_neighbor = 0
                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < size and 0 <= nc < size and board[nr][nc] == Cell_Type.MINE.value:
                        bomb_neighbor += 1

                if(board[row][col] != bomb_neighbor): return False
    return True

def heuristic(board):
    rows, cols = len(board), len(board[0])
    def get_neighbor(r, c):
        direction= [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []
        for dr, dc in direction:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors
    
    guide_ceils = []
    #Lấy ra tổ hợp (row, col, heuristic_value) của các ô chỉ dẫn
    for r in range(rows):
            for c in range(cols):
                if 0 <= board[r][c] <= 8:
                    neighbors = get_neighbor(r,c)
                    unOpened= [(nr,nc) for nr, nc in neighbors if board[nr][nc] == Cell_Type.HIDE.value]
                    bombs = [(nc,nr) for nr, nc in neighbors if board[nr][nc] == Cell_Type.MINE.value]
                    
                    remain_bombs = board[r][c] - len(bombs)
                    if remain_bombs < 0 or len(unOpened) < 0:
                        continue  # Bỏ qua trường hợp không hợp lệ

                    heuristic_value = math.comb(remain_bombs, len(unOpened)) #Lấy tổ hợp của số ô chưa mở chập số bom còn lại chưa khám phá
                    guide_ceils.append((r,c, remain_bombs, heuristic_value))

    # Sắp xếp guide_ceils theo giá trị heuristic_value
    if guide_ceils:
        guide_ceils = sorted(guide_ceils, key=lambda x: x[3])
        return guide_ceils[0]
    else:
        return None  # Trả về None nếu không có ô hợp lệ

def solve_simple_minesweeper(board):
    rows, cols = len(board), len(board[0])
    def get_neighbor(r, c):
        direction= [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        neighbors = []
        for dr, dc in direction:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
        return neighbors

    def apply_logic():
        changed = False
        for r in range(rows):
            for c in range(cols):
                if 0 <= board[r][c] <= 8:
                    neighbors = get_neighbor(r,c)
                    unOpened= [(nr,nc) for nr, nc in neighbors if board[nr][nc] == Cell_Type.HIDE.value]
                    bombs = [(nc,nr) for nr, nc in neighbors if board[nr][nc] == Cell_Type.MINE.value]

                    # Nếu ô đó là số 0 thì toàn bộ ô chưa mở xung quanh nó là an toàn
                    if board[r][c] == 0:
                        for nr, nc in unOpened:
                            board[nr][nc] = Cell_Type.EMPTY.value
                            changed = True

                    #Nếu số bom cần tìm bằng số ô chưa mở -> Tất cả các ô chưa mở là bom
                    if len(unOpened) > 0 and len(unOpened) + len(bombs) ==  board[r][c]:
                        for nr,nc in unOpened:
                            board[nr][nc] = Cell_Type.MINE.value
                            changed = True

                    # Nếu số bom đã biết = số hiển thị -> Các ô chưa mở còn lại là an toàn
                    if len(bombs) == board[r][c]:
                        for nr, nc in unOpened:
                            board[nr][nc] = Cell_Type.EMPTY.value
                            changed = True

        return changed

    while apply_logic():
        pass

    return board

def generate_bomb_cases(board, r, c, remain_bomb):
    """
    Tạo tất cả các tổ hợp có đúng `remain_bomb` quả bom trong các ô chưa mở
    xung quanh tọa độ (r, c).
    """
    rows, cols = len(board), len(board[0])
    
    # Xác định các tọa độ lân cận chưa mở
    neighbors = [
        (nr, nc)
        for nr in range(r - 1, r + 2)
        for nc in range(c - 1, c + 2)
        if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) != (r, c) and board[nr][nc] == Cell_Type.HIDE.value
    ]
    
    # Tạo tổ hợp các trường hợp có đúng `remain_bomb` quả bom
    bomb_cases = list(combinations(neighbors, remain_bomb))
    
    # Tạo danh sách lưu trữ các board mới
    new_boards = []

    for case in bomb_cases:
        # Tạo bản sao của board gốc
        new_board = [row[:] for row in board]

        # Đặt bom vào các ô trong tổ hợp
        for nr, nc in case:
            new_board[nr][nc] = Cell_Type.MINE.value

        # Thêm bản sao mới vào danh sách
        new_boards.append(new_board)

    return new_boards

def Heuristic_Search(board, game = None):
    #Đầu tiên quét sơ board và giải quyết dựa trên các luật cơ bản của trò chơi
    setting.current_state += 1
    result = solve_simple_minesweeper(board)
    if game is not None:
        game.grid.set_grid_data(result)
        game.draw_every_states()
    if check_goal_board(result): return result # Nếu thỏa mãn goal thì trả về đáp án ngay lập tức
    else:
        better_decision = heuristic(result)
        r,c,remain_bomb = better_decision[:3]

        bomb_cases = generate_bomb_cases(result,r,c,remain_bomb)
        for bomb_case in bomb_cases:
            if check_valid_board(bomb_case):
                recursive_result = Heuristic_Search(bomb_case,game)
                if recursive_result is not None:
                    return recursive_result
                
    return None