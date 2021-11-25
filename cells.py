import ray


def _get_neighbours(pos):
    """Returns the positions of the cells neighbours"""
    x = pos[0]
    y = pos[1]
    return [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1)]

@ray.remote
def _step(partial_pos, full_pos):
    """Returns a partial list of cells that should be killed and cells that should be made live"""
    already_checked = set()
    cells_to_make_live = []
    cells_to_kill = []

    for cell in partial_pos:
        x = cell[0]
        y = cell[1]
        neighbours = [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1)]
        num_live_neighbours = 0
        for neighbour in neighbours:
            if neighbour in full_pos:
                num_live_neighbours += 1
            else:
                if neighbour not in already_checked:
                    already_checked.add(neighbour)
                    nx = neighbour[0]
                    ny = neighbour[1]
                    neighbours_of_neighbours = [(nx, ny-1), (nx+1, ny-1), (nx+1, ny), (nx+1, ny+1),
                                                (nx, ny+1), (nx-1, ny+1), (nx-1, ny), (nx-1, ny-1)]
                    count = 0
                    for n in neighbours_of_neighbours:
                        if n in full_pos:
                            count = count + 1
                    if count == 3:
                        cells_to_make_live.append(neighbour)

        if num_live_neighbours < 2 or num_live_neighbours > 3:
            cells_to_kill.append((x, y))

    return cells_to_make_live, cells_to_kill


class Cells:
    """Contains methods to add, add_all, remove, remove_all, clear, get, start_step, finish_step, and step cells"""

    def __init__(self):
        self._cells = set()
        self._future = None

    def add(self, pos):
        """Adds a cell at position (x, y)"""
        assert isinstance(pos, tuple), "can not add cell using non-tuple position"
        self._cells.add(pos)

    def add_all(self, iterable):
        """Adds all cells in the iterable"""
        for pos in iterable:
            self.add(pos)

    def remove(self, pos):
        """Removes the cell at position (x, y)"""
        assert isinstance(pos, tuple), "can not remove cell using non-tuple position"
        self._cells.remove(pos)

    def remove_all(self, iterable):
        """Removes all cells in the iterable1"""
        for pos in iterable:
            self.remove(pos)

    def clear(self):
        """Removes all cells"""
        self._cells = set()

    def get(self):
        """Returns a set containing all positions, (x, y), of all cells"""
        return self._cells

    def size(self):
        """Returns the size of the cells"""
        return len(self._cells)

    def _partition(self):
        """Returns a 2d list containing positions, [x, y], of all cells grouped together
        by four cartesian planes centered about the average cell position.
        """
        res = [[] for _ in range(4)]
        length = len(self._cells)
        x_mid = 0
        y_mid = 0
        if length > 0:
            mid = [0, 0]
            for cell in self._cells:
                mid[0] += cell[0]
                mid[1] += cell[1]
            x_mid = int(mid[0] / length)
            y_mid = int(mid[1] / length)
        for cell in self._cells:
            x = cell[0]
            y = cell[1]
            if x <= x_mid and y <= y_mid:
                res[0].append([x, y])
            elif x <= x_mid and y > y_mid:
                res[1].append([x, y])
            elif x > x_mid and y <= y_mid:
                res[2].append([x, y])
            else:
                res[3].append([x, y])
        return res

    def _get_live_neighbours_count(self, pos):
        """Returns the number of live neighbors of the cell"""
        neighbours = _get_neighbours(pos)
        num_live_neighbours = 0
        for neighbour in neighbours:
            if neighbour in self._cells:
                num_live_neighbours += 1
        return num_live_neighbours

    def start_step(self):
        """Creates a future for the position of the next cells"""
        partitioned_pos = self._partition()
        full_pos = ray.put(self._cells)
        self._future = [_step.remote(partial_pos, full_pos) for partial_pos in partitioned_pos]

    def finish_step(self):
        """Waits until the results from the step are calculated
        and updates the position of the cells
        """
        res = ray.get(self._future)
        for r in res:
            self.remove_all(r[1])
            self.add_all(r[0])

    def step(self):
        """Updates the position of the cells"""
        live_cells = self._cells
        already_checked = set()
        cells_to_make_live = []
        cells_to_kill = []

        for cell in live_cells:
            neighbours = _get_neighbours(cell)
            num_live_neighbours = 0
            for neighbour in neighbours:
                if neighbour in live_cells:
                    num_live_neighbours += 1
                else:
                    if neighbour not in already_checked:
                        already_checked.add(neighbour)
                        if self._get_live_neighbours_count(neighbour) == 3:
                            cells_to_make_live.append(neighbour)

            if num_live_neighbours < 2 or num_live_neighbours > 3:
                cells_to_kill.append(cell)

        self.remove_all(cells_to_kill)
        self.add_all(cells_to_make_live)
