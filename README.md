# Smart Rescue Robot — A* Pathfinding

**Course:** Fundamentals of AI (CF321) — Search Algorithms

## Project idea
A rescue robot moves through a grid-based building to reach a person needing help. Walls cannot be crossed, while dangerous areas can be crossed at a higher cost. The robot computes a minimum-cost rescue route using the **A* search algorithm**. Users can edit the map and search again.

## State space and problem formulation
- **State:** robot position as a pair `(row, column)`.
- **Initial state:** green cell marked **R** (default `(1, 1)`).
- **Goal state:** red cell marked **G** (default `(10, 14)`).
- **Actions:** move one cell **up, down, left or right** within the grid. Diagonal motion is not allowed.
- **Walls:** dark cells; impassable.
- **Normal movement cost:** 1 for entering a normal cell.
- **Danger movement cost:** 5 for entering an orange danger cell.
- **Solution:** a continuous route from the start to the goal with minimum total movement cost.

## Algorithm and heuristic
A* evaluates nodes using `f(n) = g(n) + h(n)`, where `g(n)` is the cost of the path from the start and `h(n)` is the **Manhattan distance** to the goal:

`h(n) = abs(current_row - goal_row) + abs(current_col - goal_col)`

We chose Manhattan distance because movement is restricted to four cardinal directions. Every legal step costs at least 1, so this heuristic never overestimates the remaining cost (admissible), and it is consistent. A* with these costs finds an optimal minimum-cost route. It may take more *steps* than the shortest geometric route to avoid expensive danger.

The search uses a priority queue, best-known path costs, parent pointers, and an expanded-node set.

## How to run
**Requirements:** Python 3.9+; no pip packages required. The graphical version requires **Tkinter**, commonly included with Python desktop installations.

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Start the graphical interface:
   ```bash
   python main.py
   ```
   On macOS/Linux, use `python3` if `python` is unavailable.
4. If Tkinter is not installed or you are using a headless terminal, run:
   ```bash
   python main.py --demo
   ```

## GUI controls
Select **Wall**, **Danger**, **Erase**, **Set Start**, or **Set Goal**, then click grid cells. Press **Find Rescue Path (A*)** to calculate a new route. **Reset Example** restores the example map; **Clear Obstacles** removes walls/danger. Green = robot; red = person; blue = solution; orange = danger; dark = wall.

## Results
After running A*, the interface displays:
- Whether a route was found (or **No path found**).
- The **number of steps** (`len(path) - 1`).
- The **total movement cost**, including any danger penalties.
- The **number of nodes explored** (nodes expanded from the priority queue).

On unreachable maps the program reports no route and the number of explored nodes instead of crashing. Terminal mode prints the route coordinates, cost, and explored-node count.

## Tests
Run the standard-library unit tests:
```bash
python -m unittest discover -s tests -v
```
Tests cover shortest routes, danger avoidance, unreachable goals, blocked goals, equal start/goal, invalid grid shape, and the heuristic.

## Files
- `main.py` — interactive Tkinter interface and terminal demo.
- `algorithm.py` — independent A* implementation.
- `tests/test_algorithm.py` — unit tests.
- `TEAM.md` — team names, student IDs, and leader.

## Team
See [TEAM.md](TEAM.md).

**Team leader:** mahmoud ahmed farouk (24030114).
