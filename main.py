import heapq
import copy
import requests


class Cell(object):
    def __init__(self, x, y, reachable):

        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0


class PackageMap(object):
    def __init__(self):
        self.opened = []
        heapq.heapify(self.opened)
        self.closed = set()
        self.cells = []
        self.grid_height = None
        self.grid_width = None
        self.paths = {}

    def init(self, width, height, walls):

        self.grid_height = height
        self.grid_width = width
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in walls:
                    reachable = False
                else:
                    reachable = True
                self.cells.append(Cell(x, y, reachable))

    def get_heuristic(self, cell, end):
        return abs(cell.x - end.x) + abs(cell.y - end.y)

    def get_cell(self, x, y):
        return self.cells[x * self.grid_height + y]

    def get_adjacent_cells(self, cell):
        cells = []
        if cell.x < self.grid_width-1:
            cells.append(self.get_cell(cell.x+1, cell.y))
        if cell.y > 0:
            cells.append(self.get_cell(cell.x, cell.y-1))
        if cell.x > 0:
            cells.append(self.get_cell(cell.x-1, cell.y))
        if cell.y < self.grid_height-1:
            cells.append(self.get_cell(cell.x, cell.y+1))
        return cells

    def get_path(self, start,  end):
        cell = end
        path = [(cell.x, cell.y)]
        if start == end:
            return path
        while cell.parent and cell.parent is not start:
            cell = cell.parent
            path.append((cell.x, cell.y))

        path.append((start.x, start.y))
        path.reverse()
        return path

    def update_cell(self, adj, cell, end):

        adj.g = cell.g + 1
        adj.h = self.get_heuristic(adj, end)
        adj.parent = cell
        adj.f = adj.h + adj.g

    def find_path(self, start, end):
        start_cell = self.get_cell(*start)
        end_cell = self.get_cell(*end)
        if (start, end) not in self.paths:
            path = self.solve(start_cell, end_cell)
            path_reverse = copy.deepcopy(path)
            path_reverse.reverse()
            self.paths[(start, end)] = (path, len(path))
            self.paths[(end, start)] = (path_reverse, len(path))
        return self.paths[(start, end)]

    def solve(self, start, end):
        heapq.heappush(self.opened, (start.f, start))
        while len(self.opened):
            f, cell = heapq.heappop(self.opened)
            self.closed.add(cell)
            if cell is end:
                return self.get_path(start, end)
            adj_cells = self.get_adjacent_cells(cell)
            for adj_cell in adj_cells:
                if adj_cell.reachable and adj_cell not in self.closed:
                    if (adj_cell.f, adj_cell) in self.opened:
                        if adj_cell.g > cell.g + 1:
                            self.update_cell(adj_cell, cell, end)
                    else:
                        self.update_cell(adj_cell, cell, end)
                        heapq.heappush(self.opened, (adj_cell.f, adj_cell))


class MailMan(object):
    def __init__(self):
        self.x = 0
        self.y = 0

    def init(self):
        self.blocks = []

    def reset(self):
        self.current = (0, 0)

    def up(self):
        print 'go up'

    def down(self):
        print 'go down'

    def right(self):
        print 'go right'

    def left(self):
        print 'go left'

    def go(self, path):
        for (x, y) in path:
            if self.x != x:
                if self.x < x:
                    self.right()
                else:
                    self.left()
            elif self.y != y:
                if self.y < y:
                    self.down()
                else:
                    self.up()
            else:
                print 'start'
            self.x = x
            self.y = y

if __name__ == '__main__':
    mailman = MailMan()
    mailman.init()
    packagemap = PackageMap()
    packagemap.init(12, 12, mailman.blocks)
    path = packagemap.find_path((0, 0), (0, 0))
    print path



