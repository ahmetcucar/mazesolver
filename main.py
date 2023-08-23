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


def main():
    window = Window(800, 600)
    window.draw_line(Line(Point(0, 0), Point(800, 600)), "red")
    window.draw_line(Line(Point(0, 600), Point(800, 0)), "blue")
    window.wait_for_close()

main()