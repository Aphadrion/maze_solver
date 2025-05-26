from graphics import *

class Cell():
    def __init__(self, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1
        self.__x2 = -1
        self.__y1 = -1
        self.__y2 = -1
        self.__win = window
        self.visited = False

    def draw(self, x1, y1, x2, y2):
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

        wall_left = Line(Point(x1, y1), Point(x1, y2))
        wall_right = Line(Point(x2, y1), Point(x2, y2))
        wall_top = Line(Point(x1, y1), Point(x2,y1))
        wall_bottom = Line(Point(x1,y2), Point(x2,y2))

        if self.has_left_wall == True:
            self.__win.draw_line(wall_left)
        else:
            self.__win.draw_line(wall_left, fill_color="white")
        if self.has_right_wall == True:
            self.__win.draw_line(wall_right)
        else:
            self.__win.draw_line(wall_right, fill_color="white")
        if self.has_top_wall == True:
            self.__win.draw_line(wall_top)
        else:
            self.__win.draw_line(wall_top, fill_color="white")
        if self.has_bottom_wall == True:
            self.__win.draw_line(wall_bottom)
        else:
            self.__win.draw_line(wall_bottom, fill_color="white")

    def draw_move(self, to_cell, undo=False):
        start_center = Point(abs((self.__x1 + self.__x2)) // 2 , abs((self.__y1 + self.__y2)) // 2)
        finish_center = Point(abs((to_cell.__x1 + to_cell.__x2)) // 2, abs((to_cell.__y1 + to_cell.__y2)) // 2)
        path = Line(start_center, finish_center)
        
        fill_color = "red"
        if undo:
            fill_color = "gray"

        self.__win.draw_line(path, fill_color)
