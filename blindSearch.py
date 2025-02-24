from queue import Queue
from cell import Cell_Type
import copy
import setting

#result_board, challenge_board = generate_minesweeper_challenge(size)
#print(result_board)
#print(challenge_board)

# challenge_board=[[h,h,h,h,2,h,h],
#                  [h,1,2,1,h,2,h],
#                  [2,h,3,h,2,h,h],
#                  [2,h,h,h,h,1,1],
#                  [h,h,h,h,5,h,2],
#                  [1,2,h,h,h,h,h],
#                  [h,h,2,3,h,3,h]]

# challenge_board=[[h,h,1,h,h,h,2],
#                  [2,h,h,h,h,4,h],
#                  [2,h,2,h,2,h,2],
#                  [2,h,h,h,3,4,h],
#                  [3,h,h,3,h,h,h],
#                  [h,4,3,3,h,h,h],
#                  [h,h,h,h,h,h,0]]

# challenge_board=[[h,h,h,1,h],
#                  [h,3,4,h,2],
#                  [h,h,h,4,h],
#                  [h,h,h,4,h],
#                  [h,2,3,h,h]]

def check_valid_board(board):
    size = len(board)
    sum = 0
    for row in range(size):
        for col in range(size):
            if(board[row][col] != Cell_Type.HIDE.value and board[row][col] != Cell_Type.MINE.value):
                bomb_neighbor = 0
                if(row + 1 < size and board[row+1][col] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row - 1 >= 0 and board[row-1][col] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(col + 1 < size and board[row][col + 1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(col - 1 >= 0 and board[row][col - 1] == Cell_Type.MINE.value): bomb_neighbor += 1

                if(row + 1 < size and col - 1 >= 0 and board[row+1][col-1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row + 1 < size and col + 1 < size and board[row+1][col+1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row - 1 >= 0 and col - 1 >= 0 and board[row-1][col-1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row - 1 >= 0 and col + 1 < size and board[row-1][col+1] == Cell_Type.MINE.value): bomb_neighbor += 1

                if(board[row][col] < bomb_neighbor): return False
            if board[row][col] == Cell_Type.MINE.value: sum += 1

    # if sum > num_bomb: return False
    return True

def goal_mine_Result(board):
    size = len(board)
    for row in range(size):
        for col in range(size):
            if(board[row][col] != Cell_Type.HIDE.value and board[row][col] != Cell_Type.MINE.value):
                bomb_neighbor = 0
                if(row + 1 < size and board[row+1][col] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row - 1 >= 0 and board[row-1][col] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(col + 1 < size and board[row][col + 1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(col - 1 >= 0 and board[row][col - 1] == Cell_Type.MINE.value): bomb_neighbor += 1

                if(row + 1 < size and col - 1 >= 0 and board[row+1][col-1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row + 1 < size and col + 1 < size and board[row+1][col+1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row - 1 >= 0 and col - 1 >= 0 and board[row-1][col-1] == Cell_Type.MINE.value): bomb_neighbor += 1
                if(row - 1 >= 0 and col + 1 < size and board[row-1][col+1] == Cell_Type.MINE.value): bomb_neighbor += 1

                if(board[row][col] != bomb_neighbor): return False
    return True

def copy_board(board, row, col):
    new_board= copy.deepcopy(board)
    new_board[row][col] = Cell_Type.MINE.value

    return new_board

def BFS_Search(board, game=None):
    q = Queue()
    visited = set()

    q.put(board)
    visited.add(tuple(map(tuple, board)))
    while(not q.empty()):
        temp = q.get()
        if game is not None:
            game.grid.set_grid_data(temp)
            game.draw_every_states()
        setting.current_state += 1
        if goal_mine_Result(temp): return temp
        for row in range(len(temp)):
            for col in range(len(temp[row])):
                if(temp[row][col] == Cell_Type.HIDE.value):
                    child_board = copy_board(temp, row, col)
                    child_state = tuple(map(tuple, child_board))
                    if child_state not in visited and check_valid_board(child_board):
                        q.put(child_board)
                        visited.add(child_state)
    return None

def DFS_Search(board, game = None):
    stack = []
    visited = set()
    
    stack.append(board)
    visited.add(tuple(map(tuple, board)))

    while stack:
        temp = stack.pop()
        if game is not None:
            game.grid.set_grid_data(temp)
            game.draw_every_states()
        setting.current_state += 1
        # print(temp)
        if goal_mine_Result(temp):
            return temp
        for row in range(len(temp)):
            for col in range(len(temp[row])):
                if temp[row][col] == Cell_Type.HIDE.value:
                    child_board = copy_board(temp, row, col)
                    child_state = tuple(map(tuple, child_board))
                    if child_state not in visited and check_valid_board(child_board):
                        stack.append(child_board)
                        visited.add(child_state)

    return None