from tkinter import *
import argparse
import random


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

    def draw_line(self, line, color, width=None):
        line.draw(self.__canvas, color, width)

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

    def draw(self, canvas, color, width=None):
        w = width if width else 4
        canvas.create_line(
            self.start.x, self.start.y, self.end.x, self.end.y, fill=color, width=w
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
        # self.__window._Window__root.after(1)

    def draw_move(self, to_cell, true_color=None, undo=False, undo_color=None):
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
        c = "red"
        if true_color:
            c = true_color
        if undo:
            c = undo_color if undo_color else "gray"

        self.__window.draw_line(
            Line(self.get_center(), to_cell.get_center()), c, 10
        )

        # wait for a bit, but adjust the time depending on the amount of cells in the maze
        # self.__window._Window__root.after(75)
        self.__window.redraw()


    def check_window(self):
        if self.__window is None:
            raise Exception("Cell must have a window")


class Maze:
    def __init__(self, x, y, num_rows, num_cols, window=None, base_color=None):
        self.x = x
        self.y = y
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cells = []
        self.__window = window

        # colors
        self.base_color = base_color if base_color else "#B7B7B7"
        self.generate_color1 = "#33AFFE"
        self.generate_color2 = "white"
        self.solve_color1 = "red"
        self.solve_color2 = "gray"

        self.create()


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
                        self.base_color,
                        self.__window,
                    )
                )
            self.cells.append(row)


    def draw(self):
        self.__check_window()
        # draw + animate cells
        for r in range(len(self.cells)):
            for c in range(len(self.cells[r])):
                self.cells[r][c].draw()


    def generate(self, color1=None, color2=None):
        self.__check_window()

        if color1:
            self.generate_color1 = color1
        if color2:
            self.generate_color2 = color2
        self.__break_entrance_and_exit()
        self.__break_walls_dfs(
            random.randint(0, self.num_rows - 1),
            random.randint(0, self.num_cols - 1),
        )
        self.__reset_visited()


    def solve(self, true_color=None, undo_color=None):
        if true_color:
            self.solve_color1 = true_color
        if undo_color:
            self.solve_color2 = undo_color
        return self.__solve_dfs(0, 0)

    def __solve_dfs(self, r, c):
        if not self.__in_bounds(r, c):
            raise Exception("Cell must be in bounds")

        self.cells[r][c].visited = True

        # check if we are at the end
        if r == self.num_rows - 1 and c == self.num_cols - 1:
            return True

        # get all the neighbors of the cell and sort them by distance from the end
        neighbors = self.__get_neighbors(r, c)
        neighbors.sort(key=lambda x: abs(x[0] - (self.num_rows - 1)) + abs(x[1] - (self.num_cols - 1)))

        # enter neighbors that have not been visited and do not have a wall between them
        for neighbor in neighbors:
            nr, nc = neighbor
            if not self.cells[nr][nc].visited and not self.__has_wall(r, c, nr, nc):
                self.cells[r][c].draw_move(self.cells[nr][nc], self.solve_color1, False, self.solve_color2)
                self.__window._Window__root.after(75)
                if self.__solve_dfs(nr, nc):
                    return True
                self.cells[r][c].draw_move(self.cells[nr][nc], self.solve_color1, True, self.solve_color2)


    def __break_entrance_and_exit(self):
        self.__check_window()
        # see if we have multiple rows and columns
        if len(self.cells) > 0 and len(self.cells[0]) > 0:
            self.cells[0][0].has_left_wall = False
            self.cells[-1][-1].has_right_wall = False
            self.cells[0][0].draw()
            self.cells[-1][-1].draw()


    # generate a random maze using recursive backtracking
    def __break_walls_dfs(self, r, c):
        if not self.__in_bounds(r, c):
            raise Exception("Cell must be in bounds")

        if self.cells[r][c].visited:
            return
        self.cells[r][c].visited = True

        # get all the neighbors of the cell and randomly shuffle them
        neighbors = self.__get_neighbors(r, c)
        random.shuffle(neighbors)

        # for each neighbor, check if it has been visited
        # if it has not been visited, break the wall between the
        # current cell and the neighbor and enter the neighbor
        for neighbor in neighbors:
            nr, nc = neighbor
            if not self.cells[nr][nc].visited:
                self.__break_wall(r, c, nr, nc)
                self.cells[r][c].color = self.generate_color1
                self.cells[nr][nc].color = self.generate_color1
                self.cells[r][c].draw()
                self.cells[nr][nc].draw()
                self.__break_walls_dfs(nr, nc)

        # after all neighbors have been visited, change color back to white
        self.cells[r][c].color = self.generate_color2
        self.cells[r][c].draw()


    # check if there is a wall between the cells at (r1, c1) and (r2, c2)
    def __has_wall(self, r1, c1, r2, c2):
        if not self.__in_bounds(r1, c1) or not self.__in_bounds(r2, c2):
            raise Exception("Cells must be in bounds")

        # check if (r1, c1) and (r2, c2) are adjacent
        if r1 == r2:
            if c1 == c2 - 1:
                return self.cells[r1][c1].has_right_wall and self.cells[r2][c2].has_left_wall
            elif c1 == c2 + 1:
                return self.cells[r1][c1].has_left_wall and self.cells[r2][c2].has_right_wall
        elif c1 == c2:
            if r1 == r2 - 1:
                return self.cells[r1][c1].has_bottom_wall and self.cells[r2][c2].has_top_wall
            elif r1 == r2 + 1:
                return self.cells[r1][c1].has_top_wall and self.cells[r2][c2].has_bottom_wall
        return False


    # break the wall between the cells at (r1, c1) and (r2, c2)
    def __break_wall(self, r1, c1, r2, c2):
        if not self.__in_bounds(r1, c1) or not self.__in_bounds(r2, c2):
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


    # returns an array of tuples of the form (r, c)
    # that represent the neighbors of the cell at (row, col)
    def __get_neighbors(self, row, col):
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


    def __reset_visited(self):
        for r in range(len(self.cells)):
            for c in range(len(self.cells[r])):
                self.cells[r][c].visited = False


    def __check_window(self):
        if self.__window is None:
            raise Exception("Maze must have a window")



    # check if given cell is in bounds of the maze
    def __in_bounds(self, r, c):
        return r in range(self.num_rows) and c in range(self.num_cols)


def main():
    # create a parser
    parser = argparse.ArgumentParser(description="Generate and solve a maze")

    # add arguments to the parser with default values
    parser.add_argument(
        "-r",
        type=int,
        default=12,
        help="number of rows in the maze (default: 12)",
    )
    parser.add_argument(
        "-c",
        type=int,
        default=12,
        help="number of columns in the maze (default: 12)",
    )
    parser.add_argument(
        "-color",
        type=str,
        default=None,
        help="color of the maze generation (default: blue)",
    )
    # parse the arguments
    args = parser.parse_args()

    # access the arguments
    num_rows = args.r
    num_cols = args.c
    generate_color1 = args.color

    # create and run the maze
    window = Window(1300, 1300)
    maze = Maze(20, 20, num_rows, num_cols, window)
    maze.draw()
    maze.generate(generate_color1)
    maze.solve()
    window.wait_for_close()

main()
