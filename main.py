from tkinter import Tk, BOTH, Canvas
from time import sleep
import random

class Window:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.title = "Maze Solver"
        self.canvas = Canvas(bg="white")
        self.running = False

        self.canvas.pack()

    def redraw(self):
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self):
        self.running = True

        while self.running:
            self.redraw()

    def close(self):
        self.running = False

    def draw_line(self, line, fill_color):
        line.draw(fill_color)


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def draw(self, canvas, fill_color):
        canvas.create_line(
            self.point1.x, self.point1.y, self.point2.x, self.point2.y, fill=fill_color, width=2
            )
        canvas.pack()


class Cell:

    def __init__(self, win=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._win = win
        self.visited = False

    def draw(self):
        if self._x1 < self._x2:
            left = self._x1
            right = self._x2
        else:
            left = self._x2
            right = self._x1

        if self._y1 > self._y2:
            top = self._y1
            bottom = self._y2
        else:
            top = self._y2
            bottom = self._y1
        
        top_left = Point(left, top)
        top_right = Point(right, top)
        bottom_left = Point(left, bottom)
        bottom_right = Point(right, bottom)

        if self.has_left_wall:
            left_wall = Line(top_left, bottom_left)
            left_wall.draw(self._win.canvas, "black")
        
        if self.has_right_wall:
            right_wall = Line(top_right, bottom_right)
            right_wall.draw(self._win.canvas, "black")
        
        if self.has_top_wall:
            top_wall = Line(top_left, top_right)
            top_wall.draw(self._win.canvas, "black")

        if self.has_bottom_wall:
            bottom_wall = Line(bottom_left, bottom_right)
            bottom_wall.draw(self._win.canvas, "black")
        
        if not self.has_left_wall:
            left_wall = Line(top_left, bottom_left)
            left_wall.draw(self._win.canvas, "white")
        
        if not self.has_right_wall:
            right_wall = Line(top_right, bottom_right)
            right_wall.draw(self._win.canvas, "white")
        
        if not self.has_top_wall:
            top_wall = Line(top_left, top_right)
            top_wall.draw(self._win.canvas, "white")

        if not self.has_bottom_wall:
            bottom_wall = Line(bottom_left, bottom_right)
            bottom_wall.draw(self._win.canvas, "white")

    def draw_move(self, to_cell, undo = False):
        from_x = (self._x1 + self._x2) / 2
        from_y = (self._y1 + self._y2) / 2
        from_center = Point(from_x, from_y)

        to_x = (to_cell._x1 + to_cell._x2) / 2
        to_y = (to_cell._y1 + to_cell._y2) / 2
        to_center = Point(to_x, to_y)

        move = Line(from_center, to_center)

        if undo:
            move.draw(self._win.canvas, "gray")
        else:
            move.draw(self._win.canvas, "red")
        

class Maze:

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []
        self.seed = seed
        if seed != None:
            self.seed = random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0,0)

    def _create_cells(self):
        for i in range(self.num_cols):
            cells = []
            for j in range(self.num_rows):
                cells.append(Cell(win=self.win))
            self._cells.append(cells)
        
        for i in range(self.num_cols):
            for j in range(self.num_rows):
                self._draw_cell(i, j)
        
    def _draw_cell(self, i, j):
        cell = self._cells[i][j]

        cell._x1 = self.x1 + self.cell_size_x * i
        cell._x2 = self.x1 + self.cell_size_x * (i + 1)
        cell._y1 = self.y1 + self.cell_size_y * j
        cell._y2 = self.y1 + self.cell_size_y * (j +1)

        cell.draw()

        self._animate()

    def _animate(self):
        self.win.redraw()
        sleep(0.05)

    def _break_entrance_and_exit(self):
        maze_entrance = self._cells[0][0]
        maze_entrance.has_left_wall = False
        # maze_entrance.has_right_wall = False
        # maze_entrance.has_top_wall = False
        # maze_entrance.has_bottom_wall = False
        maze_entrance.draw()

        maze_exit = self._cells[-1][-1]
        # maze_exit.has_left_wall = False
        maze_exit.has_right_wall = False
        # maze_exit.has_top_wall = False
        # maze_exit.has_bottom_wall = False
        maze_exit.draw()

    def _break_walls_r(self, i, j):
        current_cell = self._cells[i][j]
        current_cell.visited = True

        while True:
            to_visit = []
           
            if i > 0 and not self._cells[i-1][j].visited:
                left = (i-1,j)
                to_visit.append(left)
           
            if i < self.num_cols - 1 and not self._cells[i+1][j].visited:
                right = (i+1,j)
                to_visit.append(right)
          
            if j > 0 and not self._cells[i][j-1].visited:
                top = (i, j-1)
                to_visit.append(top)
            
            if j < self.num_rows -1 and not self._cells[i][j+1].visited:
                bottom = (i, j+1)
                to_visit.append(bottom)
          
            if not to_visit:
                current_cell.draw()
                return
            
            (next_i, next_j) = random.choice(to_visit)
            next_cell = self._cells[next_i][next_j]

            if next_i == i:
                if next_j < j:
                    current_cell.has_bottom_wall = False
                    next_cell.has_top_wall = False
                else:
                    current_cell.has_top_wall = False
                    next_cell.has_bottom_wall = False
            else:
                if next_i > i:
                    current_cell.has_right_wall = False
                    next_cell.has_left_wall = False
                else:
                    current_cell.has_left_wall = False
                    next_cell.has_right_wall = False
            
            current_cell.draw()
            next_cell.draw()

            self._break_walls_r(next_i, next_j)


            


def main():
    win = Window(800, 600)

    num_cols = 5
    num_rows = 5
    m1 = Maze(2, 2, num_rows, num_cols, 20, 20, win=win)

    win.wait_for_close()

main()