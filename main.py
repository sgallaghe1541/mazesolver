from tkinter import Tk, BOTH, Canvas

class Window:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.title = "Maze Solver"
        self.canvas = Canvas()
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

    def __init__(self, window):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self._x1 = 0
        self._x2 = 0
        self._y1 = 0
        self._y2 = 0
        self._win = window

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

    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        self._cells = []

        self._create_cells()


def main():

    win = Window(800, 600)

    cell1 = Cell(10,10,20,20,win)
    cell1.draw()
    cell2 = Cell(50,50,60,60, win)
    cell2.draw()
    win.wait_for_close()

main()