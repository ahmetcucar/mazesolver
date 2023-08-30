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
        m1 = Maze(0, 0, num_rows, num_cols, "white")
        m1.create()
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
        m1 = Maze(0, 0, 10, 12, "white", None, window)
        m1.create()
        m1.break_entrance_and_exit()
        self.assertFalse(m1.cells[0][0].has_left_wall)
        self.assertFalse(m1.cells[-1][-1].has_right_wall)
        window.close()

    def test_maze_get_neighbors(self):
        m1 = Maze(0, 0, 10, 12, "white")
        m1.create()
        neighbors = m1._Maze__get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 2)
        self.assertEqual(neighbors[0],(1, 0))
        self.assertEqual(neighbors[1], (0, 1))

        neighbors = m1._Maze__get_neighbors(1, 1)
        self.assertEqual(len(neighbors), 4)
        self.assertEqual(neighbors[0], (0, 1))
        self.assertEqual(neighbors[1], (2, 1))
        self.assertEqual(neighbors[2], (1, 0))
        self.assertEqual(neighbors[3], (1, 2))


    def test_maze_break_wall(self):
        window = Window(800, 600)
        m1 = Maze(0, 0, 10, 12, "white", None, window)
        m1.create()

        # test breaking bottom wall
        m1._Maze__break_wall(0, 0, 1, 0)
        self.assertFalse(m1.cells[0][0].has_bottom_wall)
        self.assertFalse(m1.cells[1][0].has_top_wall)

        # test breaking top wall
        m1._Maze__break_wall(1, 0, 0, 0)
        self.assertFalse(m1.cells[1][0].has_top_wall)
        self.assertFalse(m1.cells[0][0].has_bottom_wall)

        # test breaking right wall
        m1._Maze__break_wall(0, 0, 0, 1)
        self.assertFalse(m1.cells[0][0].has_right_wall)
        self.assertFalse(m1.cells[0][1].has_left_wall)

        # test breaking left wall
        m1._Maze__break_wall(0, 1, 0, 0)
        self.assertFalse(m1.cells[0][1].has_left_wall)
        self.assertFalse(m1.cells[0][0].has_right_wall)

        window.close()

if __name__ == "__main__":
    unittest.main()
