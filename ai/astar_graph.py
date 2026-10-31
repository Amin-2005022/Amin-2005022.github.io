# A* Search on a GRAPH

import heapq

# The problem to solve

grid = ["S..#....",
        ".#.#.##.",
        ".#...#..",
        ".####.#.",
        "......#G"]


# ---------------------------------------------------------------
# 1. The problem: a weighted graph (numbers = step costs)
# ---------------------------------------------------------------
graph = {
    'S': {'A': 1, 'B': 4},
    'A': {'C': 2, 'D': 5},
    'B': {'D': 1},
    'C': {'G': 6},
    'D': {'G': 2},
    'G': {}
}

# Heuristic table: estimated cost from each node to G
h = {'S': 3, 'A': 2, 'B': 3, 'C': 5, 'D': 2, 'G': 0}

start, goal = 'S', 'G'

# ---------------------------------------------------------------
# 2. The problem-specific helpers  (CHANGE THESE FOR A NEW PROBLEM)
# ---------------------------------------------------------------
def neighbors(node):
    return graph[node].items()          # (next node, step cost)

def heuristic(node, goal):
    return h[node]                      # look up the table

def show(path):
    print("Path    :", " -> ".join(path))

# ---------------------------------------------------------------
# 3. A* search
# ---------------------------------------------------------------
def astar(start, goal):
    pq = [(heuristic(start, goal), 0, start, [start])]   # (f, g, node, path)
    visited = set()
    while pq:
        f, g, node, path = heapq.heappop(pq)
        if node == goal:
            return g, path, len(visited)
        if node in visited:
            continue
        visited.add(node)
        for nxt, cost in neighbors(node):
            g2 = g + cost
            heapq.heappush(pq, (g2 + heuristic(nxt, goal), g2, nxt, path + [nxt]))
    return None

# ---------------------------------------------------------------
# 4. Run the A* search
# ---------------------------------------------------------------
result = astar(start, goal)
if result is None:
    print("No path found")
else:
    cost, path, expanded = result
    print("Cost    :", cost)
    print("Expanded:", expanded)
    show(path)