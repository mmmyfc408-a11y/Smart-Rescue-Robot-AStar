"""Interactive Smart Rescue Robot GUI. Run: python main.py"""
import argparse
import tkinter as tk
from tkinter import ttk
from algorithm import EMPTY, WALL, DANGER, astar

ROWS, COLS, CELL = 12, 16, 36
START, GOAL = (1, 1), (10, 14)
DEFAULT_WALLS = {(r, 5) for r in range(1, 10) if r != 6} | {
    (r, 10) for r in range(2, 11) if r != 4
}
DEFAULT_DANGER = {(4, c) for c in range(6, 10)} | {(8, c) for c in range(11, 15)}
PALETTE = {
    EMPTY: "#f2f6fc", WALL: "#27374d", DANGER: "#ffb45d"
}


def example_grid():
    grid = [[EMPTY] * COLS for _ in range(ROWS)]
    for r, c in DEFAULT_WALLS:
        grid[r][c] = WALL
    for r, c in DEFAULT_DANGER:
        grid[r][c] = DANGER
    return grid


class RescueApp:
    def __init__(self, root):
        self.root = root
        root.title("Smart Rescue Robot | A* Pathfinding")
        root.resizable(False, False)
        self.grid = example_grid()
        self.start, self.goal = START, GOAL
        self.path = []
        self.mode = tk.StringVar(value="wall")
        self.status = tk.StringVar(value="Choose a tool, then click a cell. Press Find Rescue Path.")
        self.stats = tk.StringVar(value="Ready")
        panel = ttk.Frame(root, padding=12)
        panel.pack()
        ttk.Label(panel, text="SMART RESCUE ROBOT", font=("Arial", 17, "bold")).pack(anchor="w")
        ttk.Label(panel, text="A* search | 4 directions | normal cost 1 | danger cost 5").pack(anchor="w")
        tools = ttk.Frame(panel)
        tools.pack(fill="x", pady=(10, 8))
        for text, value in [
            ("Wall", "wall"), ("Danger", "danger"), ("Erase", "erase"),
            ("Set Start", "start"), ("Set Goal", "goal")
        ]:
            ttk.Radiobutton(tools, text=text, value=value, variable=self.mode).pack(side="left", padx=4)
        self.canvas = tk.Canvas(panel, width=COLS * CELL, height=ROWS * CELL,
                                bg="white", highlightthickness=0)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.clicked)
        buttons = ttk.Frame(panel)
        buttons.pack(fill="x", pady=10)
        ttk.Button(buttons, text="Find Rescue Path (A*)", command=self.find_path).pack(side="left")
        ttk.Button(buttons, text="Reset Example", command=self.reset).pack(side="left", padx=8)
        ttk.Button(buttons, text="Clear Obstacles", command=self.clear).pack(side="left")
        ttk.Label(panel, textvariable=self.stats, font=("Arial", 11, "bold")).pack(anchor="w")
        ttk.Label(panel, textvariable=self.status, wraplength=COLS * CELL).pack(anchor="w", pady=(5, 0))
        ttk.Label(panel, text="Legend: green = start (robot) | red = goal (person) | orange = danger | dark = wall | blue = path").pack(anchor="w", pady=(6, 0))
        self.draw()

    def reset(self):
        self.grid = example_grid()
        self.start, self.goal = START, GOAL
        self.path = []
        self.stats.set("Ready")
        self.status.set("Example restored. Press Find Rescue Path.")
        self.draw()

    def clear(self):
        self.grid = [[EMPTY] * COLS for _ in range(ROWS)]
        self.path = []
        self.stats.set("Ready")
        self.status.set("Obstacles cleared.")
        self.draw()

    def clicked(self, event):
        r, c = event.y // CELL, event.x // CELL
        if not (0 <= r < ROWS and 0 <= c < COLS):
            return
        pos = (r, c)
        mode = self.mode.get()
        if mode == "start":
            if pos == self.goal:
                self.status.set("Start and goal must be different.")
                return
            self.start = pos
            self.grid[r][c] = EMPTY
        elif mode == "goal":
            if pos == self.start:
                self.status.set("Start and goal must be different.")
                return
            self.goal = pos
            self.grid[r][c] = EMPTY
        elif pos in (self.start, self.goal):
            self.status.set("Move start/goal before editing that cell.")
            return
        else:
            self.grid[r][c] = {"wall": WALL, "danger": DANGER, "erase": EMPTY}[mode]
        self.path = []
        self.stats.set("Map edited — run A* again")
        self.status.set("Map updated.")
        self.draw()

    def find_path(self):
        result = astar(self.grid, self.start, self.goal)
        self.path = result["path"] or []
        if result["path"] is None:
            self.stats.set(f"No path found | Explored nodes: {result['explored']}")
            self.status.set("Rescue is unreachable. Remove some walls and try again.")
        else:
            moves = len(result["path"]) - 1
            self.stats.set(
                f"Path found | Steps: {moves} | Cost: {result['cost']} "
                f"| Explored nodes: {result['explored']}"
            )
            self.status.set("Optimal safe-cost path shown in blue. Orange cells cost 5 to enter.")
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        path_set = set(self.path)
        for r in range(ROWS):
            for c in range(COLS):
                pos = (r, c)
                color = PALETTE[self.grid[r][c]]
                if pos in path_set:
                    color = "#70b9f5"
                if pos == self.start:
                    color = "#4ecb86"
                if pos == self.goal:
                    color = "#fa6b71"
                x, y = c * CELL, r * CELL
                self.canvas.create_rectangle(x, y, x + CELL, y + CELL,
                                             fill=color, outline="#ffffff")
                label = "R" if pos == self.start else ("G" if pos == self.goal else "")
                if label:
                    self.canvas.create_text(x + CELL / 2, y + CELL / 2,
                                            text=label, font=("Arial", 13, "bold"))


def demo():
    result = astar(example_grid(), START, GOAL)
    print("Smart Rescue Robot — A* demo")
    print("Start:", START, "Goal:", GOAL)
    print("Path:", result["path"])
    print("Cost:", result["cost"], "| Explored:", result["explored"])
    if result["path"] is None:
        print("No rescue route exists.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Smart Rescue Robot with A* search")
    parser.add_argument("--demo", action="store_true", help="Run in terminal (no GUI)")
    args = parser.parse_args()
    if args.demo:
        demo()
    else:
        window = tk.Tk()
        RescueApp(window)
        window.mainloop()
