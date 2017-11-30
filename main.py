import heapq
import copy
import requests
import time

class Cell(object):
    def __init__(self, x, y, reachable):

        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0
        self.value = 0

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
        value = 0
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

    def update_package(self, packages):
        for x, y, value in packages:
            cell = self.get_cell(x, y)
            cell.value = value

    def find_path(self, start, end):
        start_cell = self.get_cell(*start)
        end_cell = self.get_cell(*end)
        if (start, end) not in self.paths:
            path = self.solve(start_cell, end_cell)
            if not path:
                return []
            path_reverse = copy.deepcopy(path)
            path_reverse.reverse()
            self.paths[(start, end)] = (path, len(path))
            self.paths[(end, start)] = (path_reverse, len(path))
        return self.paths[(start, end)]

    def get_weight(self, start, end):
        end_cell = self.get_cell(*end)
        path = self.find_path(start, end)
        return end_cell.value -path[1]-1

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


class DoneException(Exception):
    pass


class MailMan(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.count = 0

    def init(self):
        self.blocks = []
        self.packages = [(1,1,10), (5,6,10)]
        self.packagemap = PackageMap()
        self.packagemap.init(12, 12, mailman.blocks)
        self.packagemap.update_package(self.packages)

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

    def get_length(self, path):
        i = 0
        total_length = 0
        while i < len(path) - 2:
            p = self.packagemap.find_path(path[i], path[i+1])
            total_length = total_length + p[1]
        return total_length

    def dfs_paths(self, graph, start):
        stack = [(start, [start], 0)]
        while stack:
            (vertex, path, value) = stack.pop()
            for next in graph[vertex] - set(path):
                length = self.get_length(path)
                if next[2] - length <= 0:
                    yield path, value
                else:
                    value = value + vertex.value - length
                    stack.append((next, path + [next], value))

    def build_graph(self):
        graph = {}
        for p in self.packages:
            graph[p] = set(self.packages - set(p))

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

    def run(self):
        pass

    def add_new_package(self, x, y):
        self.packages.append((x, y))

    def choose(self):
        pass

def test():
    a = PackageMap()
    walls = ((0, 5), (1, 0), (1, 1), (1, 5), (2, 3),
             (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
    walls2 = ((0, 5), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5),
             (2, 3), (3, 1), (3, 2), (3, 5), (4, 1), (4, 4), (5, 1))
    a.init(12, 12, walls)
    path = a.find_path((0, 0), (5, 5))
    path2 = a.find_path((5, 5), (0, 0))
    print path
    print path2
    man = MailMan()
    #man.go(path[0])

if __name__ == '__main__':
    mailman = MailMan()
    mailman.init()
    mailman.run()
    t1 = time.time()
    print t1
    test()
    t2 = time.time()
    print t2
    print t2 - t1



