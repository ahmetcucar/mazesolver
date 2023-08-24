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
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, "white", None)
        m1.create()
        print(f"cols: {len(m1.cells)}, rows: {len(m1.cells[0])}")
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )

    def test_maze_break_entrance_and_exit(self):
        window = Window(800, 600)
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, "white", window)
        m1.create()
        m1.break_entrance_and_exit()
        self.assertFalse(m1.cells[0][0].has_left_wall)
        self.assertFalse(m1.cells[-1][-1].has_right_wall)
        window.close()

if __name__ == "__main__":
    unittest.main()
