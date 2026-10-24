from collections import deque

graph = {
    'S': ['A', 'B'],
    'A': ['C', 'D'],
    'B': ['D'],
    'C': ['G'],
    'D': ['G'],
    'G': []
}

def bfs(graph, start, goal):
    

    return None  # No path found

print(bfs(graph, 'S', 'G'))
