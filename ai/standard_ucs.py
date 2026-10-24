import heapq

graph = {
    'S': {'A': 1, 'B': 4},
    'A': {'C': 2, 'D': 5},
    'B': {'D': 1},
    'C': {'G': 6},
    'D': {'G': 2},
    'G': {}
}

def standard_ucs(graph, start, goal):
   
    pq = [(0, start)]
    best_cost = {start: 0}
    parent = {start: None}
    explored = set()

    while pq:
        cost, node = heapq.heappop(pq)

        # Skip stale entries: a cheaper route to this node was already expanded
        if node in explored:
            continue

        # Goal test when popped (not when discovered), so the cost is the cheapest
        if node == goal:
            path = []
            curr = goal
            while curr is not None:
                path.append(curr)
                curr = parent[curr]
            return cost, path[::-1]  # Reverse to get start -> goal

        explored.add(node)

        for nb, w in graph[node].items():
            new_cost = cost + w
            # Push only if this is the first route or a cheaper route to nb
            if nb not in best_cost or new_cost < best_cost[nb]:
                best_cost[nb] = new_cost
                parent[nb] = node  # Remember the cheaper way we came from
                heapq.heappush(pq, (new_cost, nb))

    return None  # No path found

cost, path = standard_ucs(graph, 'S', 'G')
print("Standard UCS path S -> G:", path, "cost", cost)
