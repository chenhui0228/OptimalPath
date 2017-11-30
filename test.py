graph = {'A': set(['A', 'B', 'F', 'D', 'E', 'C']),
         'B': set(['A', 'B', 'F', 'D', 'E', 'C']),
         'C': set(['A', 'B', 'F', 'D', 'E', 'C']),
         'D': set(['A', 'B', 'F', 'D', 'E', 'C']),
         'E': set(['A', 'B', 'F', 'D', 'E', 'C']),
         'F': set(['A', 'B', 'F', 'D', 'E', 'C'])
         }

def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == goal:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

import time
t1 = time.time()
print list(dfs_paths(graph, 'A', 'F'))
t2 = time.time()
print t2 - t1


packages = [(1,1,10), (5,6,10)]
for package in packages:
    print package