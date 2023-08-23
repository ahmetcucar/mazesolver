from tkinter import *

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("Title")
        self.__root.geometry(f"{self.__width}x{self.__height}")
        self.__canvas = Canvas(self.__root, width=self.__width, height=self.__height)
        self.__canvas.pack()
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def draw_line(self, line, color):
        line.draw(self.__canvas, color)

    def redraw(self):
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self):
        self.__running = False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, color):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=color, width=2
        )
        canvas.pack()

class Cell:
    def __init__(self, left, right, top, bottom, x1, y1, x2, y2, window):
        self.has_left_wall = left
        self.has_right_wall = right
        self.has_top_wall = top
        self.has_bottom_wall = bottom
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.__window = window

    def get_center(self):
        return Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)

    def draw(self):
        if self.has_left_wall:
            self.__window.draw_line(
                Line(Point(self.__x1, self.__y1), Point(self.__x1, self.__y2)), "black"
            )
        if self.has_right_wall:
            self.__window.draw_line(
                Line(Point(self.__x2, self.__y1), Point(self.__x2, self.__y2)), "black"
            )
        if self.has_top_wall:
            self.__window.draw_line(
                Line(Point(self.__x1, self.__y1), Point(self.__x2, self.__y1)), "black"
            )
        if self.has_bottom_wall:
            self.__window.draw_line(
                Line(Point(self.__x1, self.__y2), Point(self.__x2, self.__y2)), "black"
            )

    def draw_move(self, to_cell, undo=False):
        # determine the positioning of to_cell relative to self and see if
        # there is a wall blocking us
        x_diff = to_cell.get_center().x - self.get_center().x
        y_diff = to_cell.get_center().y - self.get_center().y
        if x_diff != 0 and y_diff != 0:
            raise Exception("Can only move to adjacent cells")
        if x_diff == 0:
            if y_diff < 0 and self.has_top_wall:
                raise Exception("Wall in the way")
            if y_diff > 0 and self.has_bottom_wall:
                raise Exception("Wall in the way")
        else:
            if x_diff < 0 and self.has_left_wall:
                raise Exception("Wall in the way")
            if x_diff > 0 and self.has_right_wall:
                raise Exception("Wall in the way")

        # draw the line
        color = "gray" if undo else "red"
        self.__window.draw_line(
            Line(self.get_center(), to_cell.get_center()), color
        )


def main():
    window = Window(800, 600)

    # create the cells to fill the window, each having any number of walls
    cells = []
    cell_width = 200
    cell_height = 200
    for x in range(0, window._Window__width, cell_width):
        for y in range(0, window._Window__height, cell_height):
            cells.append(
                Cell(
                    True,
                    True,
                    True,
                    True,
                    x,
                    y,
                    x + cell_width,
                    y + cell_height,
                    window,
                )
            )
    for cell in cells:
        cell.draw()


    window.wait_for_close()

main()