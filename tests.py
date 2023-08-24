import unittest

# import code to be tested
from main import *

class Test(unittest.TestCase):
    # CELL TESTS

    # test cell get_center method
    def test_cell_get_center(self):
        cell = Cell(0, 0, 10, 10, "white", None)
        self.assertEqual(cell.get_center(), Point(5, 5))

        cell = Cell(10, 10, 20, 20, "white", None)
        self.assertEqual(cell.get_center(), Point(15, 15))

        cell = Cell(0, 0, 20, 20, "white", None)
        self.assertEqual(cell.get_center(), Point(10, 10))

    # MAZE TESTS

    def test_maze_create_cells(self):
        window = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, "white", window)
        self.assertEqual(
            m1.num_cols,
            num_cols,
        )
        self.assertEqual(
            m1.num_rows,
            num_rows,
        )

if __name__ == "__main__":
    unittest.main()
