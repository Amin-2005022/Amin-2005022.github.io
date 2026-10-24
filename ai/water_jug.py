from collections import deque

def get_neighbors(state, cap_a, cap_b):
    a, b = state
    pour_ab = min(a, cap_b - b)          # pour A -> B
    pour_ba = min(b, cap_a - a)          # pour B -> A
    return [(cap_a, b), (a, cap_b),      # fill A, fill B
            (0, b), (a, 0),              # empty A, empty B
            (a - pour_ab, b + pour_ab),  # pour A -> B
            (a + pour_ba, b - pour_ba)]  # pour B -> A

def water_jug(cap_a=4, cap_b=3, goal=2):
    start = (0, 0)

    if start[0] == goal:
        return [start]

    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
        state = queue.popleft()

        for nb in get_neighbors(state, cap_a, cap_b):
            if nb not in visited:
                visited.add(nb)
                parent[nb] = state 

                
                if nb[0] == goal:
                    path = []
                    curr = nb
                    while curr is not None:
                        path.append(curr)
                        curr = parent[curr]
                    return path[::-1] 

                queue.append(nb)

    return None  # No solution

print("Standard Water Jug solution:", water_jug())
