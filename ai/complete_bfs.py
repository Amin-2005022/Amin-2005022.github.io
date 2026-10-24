from collections import deque

graph = {
    'S': ['A', 'B'],
    'A': ['C', 'D'],
    'B': ['D'],
    'C': ['G'],
    'D': ['G'],
    'G': []
}

def standard_bfs(graph, start, goal):
    if start == goal:
        return [start]


    queue = deque([(start, None)])
    visited = {start}
    parent = {start: None}

    while queue:
        node, _ = queue.popleft()

        
        for nb in graph[node]:
            if nb not in visited:
                visited.add(nb)
                parent[nb] = node
                if nb == goal:
                    path = []
                    curr = goal
                    while curr is not None:
                        path.append(curr)
                        curr = parent[curr]
                    return path[::-1]
                queue.append((nb, node))

    return None 

print("Standard BFS path S -> G:", standard_bfs(graph, 'S', 'G'))
