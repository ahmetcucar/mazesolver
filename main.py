from collections import deque
import random
from tkinter import *

class Window:
    def __init__(self, width, height):
        self.__width = width
        self.__height = height
        self.__root = Tk()
        self.__root.title("Maze Solver!")
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

    def __eq__(self, other_point):
        return self.x == other_point.x and self.y == other_point.y

class Line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def draw(self, canvas, color):
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=color, width=4
        )
        canvas.pack()

class Cell:
    def __init__(self, x1, y1, x2, y2, color, window=None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = x1
        self.__y1 = y1
        self.__x2 = x2
        self.__y2 = y2
        self.color = color
        self.visited = False
        self.__window = window

    def get_center(self):
        return Point((self.__x1 + self.__x2) / 2, (self.__y1 + self.__y2) / 2)

    def draw(self):
        self.check_window()

        top_left = Point(self.__x1, self.__y1)
        top_right = Point(self.__x2, self.__y1)
        bottom_left = Point(self.__x1, self.__y2)
        bottom_right = Point(self.__x2, self.__y2)

        # fill the color of the cell with no edge color
        self.__window._Window__canvas.create_rectangle(
            self.__x1 + 1,
            self.__y1 + 1,
            self.__x2 - 1,
            self.__y2 - 1,
            fill=self.color,
            outline=self.color,
        )

        # draw the walls, depending on whether they exist or not
        self.__window.draw_line(
            Line(top_left, bottom_left),
            "black" if self.has_left_wall else self.color
        )
        self.__window.draw_line(
            Line(top_right, bottom_right),
            "black" if self.has_right_wall else self.color
        )
        self.__window.draw_line(
            Line(top_left, top_right),
            "black" if self.has_top_wall else self.color
        )
        self.__window.draw_line(
            Line(bottom_left, bottom_right),
            "black" if self.has_bottom_wall else self.color
        )

        self.__window.redraw()
        self.__window._Window__root.after(1)

    def draw_move(self, to_cell, undo=False):
        self.check_window()

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

    def check_window(self):
        if self.__window is None:
            raise Exception("Cell must have a window")

class Maze:
    def __init__(self, x, y, num_rows, num_cols, color, seed=None, window=None):
        self.x = x
        self.y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.color = color
        self.seed = seed
        self.cells = []
        self.__window = window


    def create(self):
        if self.__window:
            avail_width = self.__window._Window__width - (self.x * 2)
            avail_height = self.__window._Window__height - (self.y * 2)
            cell_width =  avail_width // self.num_cols
            cell_height = avail_height // self.num_rows
        else:
            cell_width = 20
            cell_height = 20
            avail_width = self.num_cols * cell_width
            avail_height = self.num_rows * cell_height

        # create cells
        for y in range(self.y, avail_height, cell_height):
            row = []
            for x in range(self.x, avail_width, cell_width):
                row.append(
                    Cell(
                        x,
                        y,
                        x + cell_width,
                        y + cell_height,
                        self.color,
                        self.__window,
                    )
                )
            self.cells.append(row)


    def draw(self):
        self.__check_window()

        # draw + animate cells
        for r in range(len(self.cells)):
            for c in range(len(self.cells[r])):
                print(f"drawing cell {r}, {c}")
                self.cells[r][c].draw()
                self.__window._Window__root.after(1)


    def break_entrance_and_exit(self):
        self.__check_window()

        # see if we have multiple rows and columns
        if len(self.cells) > 0 and len(self.cells[0]) > 0:
            self.cells[0][0].has_left_wall = False
            self.cells[-1][-1].has_right_wall = False
            self.cells[0][0].draw()
            self.cells[-1][-1].draw()


    # # create the maze randomly, creating a path from the starting cell
    # # to the ending cell
    def break_walls_bfs(self):
        if len(self.cells) == 0 or len(self.cells[0]) == 0:
            raise Exception("Maze must have cells")

        # create a queue of cells to visit
        queue = deque()
        queue.append(tuple([0, 0]))

        while queue:
            r, c = queue.popleft()
            print(r, c)
            self.cells[r][c].visited = True

            # get all the neighbors of the cell and randomly shuffle them
            neighbors = self.__get_neighbors(r, c)
            random.shuffle(neighbors)

            # for each neighbor, check if it has been visited
            # if it has not been visited, break the wall between the
            # current cell and the neighbor and add the neighbor to the queue
            for neighbor in neighbors:
                nr, nc = neighbor
                if not self.cells[nr][nc].visited:
                    self.__break_wall(r, c, nr, nc)
                    self.cells[nr][nc].visited = True
                    print("   -  breaking wall: ", r, c, nr, nc)
                    self.cells[r][c].draw()
                    self.cells[nr][nc].draw()
                    self.__window._Window__root.after(500)
                    queue.append(neighbor)


    def __break_wall(self, r1, c1, r2, c2):
        # check if (r1, c1) and (r2, c2) are in bounds
        if (r1 not in range(self.num_rows)
            or r2 not in range(self.num_rows)
            or c1 not in range(self.num_cols)
            or c2 not in range(self.num_cols)
        ):
            raise Exception("Cells must be in bounds")

        # break the wall between the cells at (r1, c1) and (r2, c2)
        # if they are adjacent
        if r1 == r2:
            if c1 == c2 - 1: # c1 is to the left of c2
                self.cells[r1][c1].has_right_wall = False
                self.cells[r1][c2].has_left_wall = False

            elif c1 == c2 + 1: # c1 is to the right of c2
                self.cells[r1][c1].has_left_wall = False
                self.cells[r1][c2].has_right_wall = False

        elif c1 == c2:
            if r1 == r2 - 1: # r1 is above r2
                self.cells[r1][c1].has_bottom_wall = False
                self.cells[r2][c1].has_top_wall = False

            elif r1 == r2 + 1: # r1 is below r2
                self.cells[r1][c1].has_top_wall = False
                self.cells[r2][c1].has_bottom_wall = False


    def __get_neighbors(self, row, col):
        # returns an array of tuples of the form (row, col)
        # that represent the neighbors of the cell at (row, col)
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < self.num_rows - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.num_cols - 1:
            neighbors.append((row, col + 1))
        return neighbors

    def __check_window(self):
        if self.__window is None:
            raise Exception("Maze must have a window")


def main():
    window = Window(800, 800)
    maze = Maze(20, 20, 10, 10, "white", None, window)
    maze.create()
    maze.draw()
    maze.break_entrance_and_exit()
    maze.break_walls_bfs()
    # maze.traverse_and_break()
    # maze.traverse_and_break2()


    window.wait_for_close()

main()
