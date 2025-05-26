from cell import *
from graphics import *
import random
import time

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.__cells = []
        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win

        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)
        self.__reset_cells_visited(num_cols, num_rows)

        if seed:
            random.seed(seed)

    def __create_cells(self):
        for i in range(self.__num_cols):
            col_cells = []
            for j in range(self.__num_rows):
                col_cells.append(Cell(self.__win))
            self.__cells.append(col_cells)
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)

    def __draw_cell(self, i, j):
        if self.__win is None:
            return
        x1 = self.__x1 + i * self.__cell_size_x
        y1 = self.__y1 + j * self.__cell_size_y
        x2 = x1 + self.__cell_size_x
        y2 = y1 + self.__cell_size_y
        self.__cells[i][j].draw(x1, y1, x2, y2)
        self.__animate()

    def __animate(self):
        if self.__win is None:
            return
        self.__win.redraw()
        time.sleep(0.02)

    def __break_entrance_and_exit(self):
        self.__cells[0][0].has_top_wall = False
        self.__draw_cell(0,0)
        self.__cells[self.__num_cols - 1][self.__num_rows - 1].has_bottom_wall = False
        self.__draw_cell(self.__num_cols -1, self.__num_rows - 1)

    def __break_walls_r(self, i, j):
        self.__cells[i][j].visited = True
        while True:
            next_index_list = []

            # determine which cell(s) to visit next
            # left
            if i > 0 and not self.__cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self.__cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            # if there is nowhere to go from here
            # just break out
            if len(next_index_list) == 0:
                self.__draw_cell(i, j)
                return

            # randomly choose the next direction to go
            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            # recursively visit the next cell
            self.__break_walls_r(next_index[0], next_index[1])

    '''
    def __break_walls_r(self, i ,j):
        current_cell = self.__cells[i][j]
        current_cell.visited = True
        while True:
            queue = []
            
            top_cell = self.__cells[i][j - 1]
            right_cell = self.__cells[i + 1][j]
            bottom_cell = self.__cells[i][j + 1]
            left_cell = self.__cells[i - 1][j]

            if i > 0 and not left_cell.visited:
                queue.append((i - 1, j))
           
            if i < self.__num_cols - 1 and not right_cell.visited:
                queue.append((i + 1, j))
            
            if j > 0 and not top_cell.visited:
                queue.append((i, j - 1))
            
            if j < self.__num_rows - 1 and not bottom_cell.visited:
                queue.append((i, j + 1))

            if len(queue) == 0:
                self.__draw_cell(i, j)
                return

            # randomly choose the next direction to go
            chosen = random.randrange(len(queue))
            next_index = queue[chosen]

            # knock out walls between this cell and the next cell(s)
            # right
            if next_index[0] == i + 1:
                current_cell.has_right_wall = False
                right_cell.has_left_wall = False
            # left
            if next_index[0] == i - 1:
                current_cell.has_left_wall = False
                left_cell.has_right_wall = False
            # down
            if next_index[1] == j + 1:
                current_cell.has_bottom_wall = False
                bottom_cell.has_top_wall = False
            # up
            if next_index[1] == j - 1:
                current_cell.has_top_wall = False
                top_cell.has_bottom_wall = False

            # recursively visit the next cell
            self.__break_walls_r(next_index[0], next_index[1])
    '''
            

    def __reset_cells_visited(self, num_cols, num_rows):
        for i in range(num_cols):
            for j in range(num_rows):
                self.__cells[i][j].visited = False

    def _solve_r(self, i, j):
        self.__animate()
        current_cell = self.__cells[i][j]
        current_cell.visited = True

        if current_cell == self.__cells[self.__num_cols - 1][self.__num_rows - 1]:
            return True
        
        #check right
        if i < self.__num_cols - 1:
            right_cell = self.__cells[i + 1][j]
            if not current_cell.has_right_wall and not right_cell.visited:
                current_cell.draw_move(right_cell)
                if self._solve_r(i + 1, j):
                    return True
                else:
                    current_cell.draw_move(right_cell, True)
        
        #check left
        if i > 0:
            left_cell = self.__cells[i - 1][j]
            if not current_cell.has_left_wall and not left_cell.visited:
                current_cell.draw_move(left_cell)
                if self._solve_r(i - 1, j):
                    return True
                else:
                    current_cell.draw_move(left_cell, True)

        #check top
        if j > 0:
            top_cell = self.__cells[i][j - 1]
            if not current_cell.has_top_wall and not top_cell.visited:
                current_cell.draw_move(top_cell)
                if self._solve_r(i, j - 1):
                    return True
                else:
                    current_cell.draw_move(top_cell, True)

        #check bottom
        if  j < self.__num_rows - 1:
            bottom_cell = self.__cells[i][j + 1]
            if not current_cell.has_bottom_wall and not bottom_cell.visited:
                current_cell.draw_move(bottom_cell)
                if self._solve_r(i, j + 1):
                    return True
                else:
                    current_cell.draw_move(bottom_cell, True)

        return False
    
    def solve(self):
        return self._solve_r(0, 0)
