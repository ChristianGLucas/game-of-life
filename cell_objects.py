from cells import Cells


class CellObjects:

    def __init__(self):
        self._cell_object = []
        self._cells = Cells()

    def make_glider(self, pos):
        x, y = pos
        self._cell_object = [(x, y), (x - 1, y - 1), (x, y + 1), (x + 1, y), (x - 1, y + 1)]

    def make_light_weight_spaceship(self, pos):
        x, y = pos
        self._cell_object = [(x + 1, y - 1), (x - 2, y - 1), (x + 2, y), (x + 2, y + 1),
                             (x + 2, y + 2), (x + 1, y + 2), (x, y + 2), (x - 1, y + 2), (x - 2, y + 1)]

    def make_gosper_glider_gun(self, pos):
        x, y = pos
        self._cell_object = [(x + 2, y), (x + 2, y - 1), (x + 2, y + 1), (x + 3, y), (x + 3, y + 1), (x + 3, y - 1),
                             (x + 4, y + 2), (x + 4, y - 2), (x + 6, y + 2), (x + 6, y - 2), (x + 6, y + 3),
                             (x + 6, y - 3), (x + 16, y), (x + 16, y-1), (x + 17, y), (x + 17, y - 1), (x - 1, y + 2),
                             (x - 2, y + 2), (x - 2, y + 1), (x - 2, y + 3), (x - 3, y), (x - 3, y + 4), (x - 4, y + 2),
                             (x - 5, y - 1), (x - 5, y + 5), (x - 6, y - 1), (x - 6, y + 5), (x - 7, y), (x - 7, y + 4),
                             (x - 8, y + 1), (x - 8, y + 3), (x - 8, y + 2), (x - 17, y + 1), (x - 17, y + 2),
                             (x-18, y+1), (x-18, y+2)]

    def make_acorn(self, pos):
        x, y = pos
        self._cell_object = [(x, y), (x + 1, y + 1), (x + 2, y + 1), (x + 3, y + 1),
                             (x - 2, y - 1), (x - 2, y + 1), (x - 3, y + 1)]

    def get(self):
        """Returns the cells of the cell object"""
        self._cells.add_all(self._cell_object)
        res = self._cells.get()
        self._cells.clear()
        return res

    def add(self, cells):
        """Adds a cell object to a cells class"""
        assert isinstance(cells, Cells), "can only add a cell object to a cells class"
        cells.add_all(self._cell_object)

    def update_position(self, pos):
        """Updates all of the cells positions of the cell object"""
        delta_x = pos[0] - self._cell_object[0][0]
        delta_y = pos[1] - self._cell_object[0][1]
        for i in range(len(self._cell_object)):
            cell_pos = self._cell_object[i]
            self._cell_object[i] = (cell_pos[0] + delta_x, cell_pos[1] + delta_y)

    def rotate(self, clockwise):
        """Rotates the cell object clockwise if bool is true, counter clockwise if bool is false"""
        if clockwise:
            direction = 1
        else:
            direction = -1
        for i in range(len(self._cell_object)):
            cell_pos = self._cell_object[i]
            self._cell_object[i] = (-direction * cell_pos[1], direction * cell_pos[0])