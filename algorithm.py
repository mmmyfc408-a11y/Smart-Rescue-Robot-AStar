"""A* pathfinding for a rescue robot on a four-directional grid."""
import heapq
from itertools import count

EMPTY, WALL, DANGER = 0, 1, 2
DANGER_COST = 5
MOVES = ((-1, 0), (1, 0), (0, -1), (0, 1))


def manhattan(a, b):
    """Admissible/consistent heuristic: at least one cost unit per move."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid, start, goal):
    """Return {'path': list|None, 'cost': int|None, 'explored': int}.

    grid is rectangular and contains EMPTY (0), WALL (1), or DANGER (2).
    Entering an ordinary cell costs 1; entering a dangerous cell costs 5.
    Only up/down/left/right moves are permitted. Expanded nodes are counted.
    """
    if not grid or not grid[0] or any(len(row) != len(grid[0]) for row in grid):
        raise ValueError("The grid must be non-empty and rectangular.")
    rows, cols = len(grid), len(grid[0])
    def inside(p):
        return 0 <= p[0] < rows and 0 <= p[1] < cols
    if not inside(start) or not inside(goal):
        raise ValueError("Start and goal must be inside the grid.")
    if grid[start[0]][start[1]] == WALL or grid[goal[0]][goal[1]] == WALL:
        return {"path": None, "cost": None, "explored": 0}
    if start == goal:
        return {"path": [start], "cost": 0, "explored": 1}

    counter = count()
    frontier = [(manhattan(start, goal), 0, next(counter), start)]
    g_score = {start: 0}
    parent = {}
    closed = set()
    explored = 0

    while frontier:
        _, cost, _, current = heapq.heappop(frontier)
        if current in closed or cost != g_score[current]:
            continue
        closed.add(current)
        explored += 1
        if current == goal:
            path = [current]
            while current in parent:
                current = parent[current]
                path.append(current)
            path.reverse()
            return {"path": path, "cost": cost, "explored": explored}
        for dr, dc in MOVES:
            neighbor = (current[0] + dr, current[1] + dc)
            if not inside(neighbor) or grid[neighbor[0]][neighbor[1]] == WALL:
                continue
            step = DANGER_COST if grid[neighbor[0]][neighbor[1]] == DANGER else 1
            tentative = cost + step
            if tentative < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative
                parent[neighbor] = current
                heapq.heappush(frontier, (tentative + manhattan(neighbor, goal),
                                           tentative, next(counter), neighbor))
                # A consistent heuristic makes reopening closed nodes unnecessary.
    return {"path": None, "cost": None, "explored": explored}
