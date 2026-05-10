"""
🐍 贪吃蛇游戏 - tkinter 版
运行：python snake_game.py
操作：WASD 或方向键，P 暂停，R 重开，Q 退出
"""

import tkinter as tk
import random

CELL     = 22
COLS     = 28
ROWS     = 24
W        = COLS * CELL
H        = ROWS * CELL
FPS_BASE = 130
FPS_MIN  = 55

BG         = "#0d1117"
GRID_COLOR = "#161b22"
HEAD_COLOR = "#39d353"
BODY_COLOR = "#26a641"
BODY_DARK  = "#1a7f37"
FOOD_COLOR = "#ff6b6b"
FOOD_GLOW  = "#ff4444"
WALL_COLOR = "#30363d"
TEXT_COLOR = "#e6edf3"
DIM_COLOR  = "#8b949e"
SCORE_CLR  = "#f0883e"
LEVEL_CLR  = "#79c0ff"

UP    = ( 0, -1)
DOWN  = ( 0,  1)
LEFT  = (-1,  0)
RIGHT = ( 1,  0)
OPPOSITE = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🐍 贪吃蛇")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        top = tk.Frame(root, bg=BG, pady=8)
        top.pack(fill="x", padx=16)
        tk.Label(top, text="SNAKE", font=("Courier New", 13, "bold"),
                 fg=HEAD_COLOR, bg=BG).pack(side="left")
        self.lbl_score = tk.Label(top, text="SCORE  0",
                                  font=("Courier New", 11), fg=SCORE_CLR, bg=BG)
        self.lbl_score.pack(side="left", padx=20)
        self.lbl_best = tk.Label(top, text="BEST  0",
                                 font=("Courier New", 11), fg=DIM_COLOR, bg=BG)
        self.lbl_best.pack(side="left")
        self.lbl_level = tk.Label(top, text="LV 1",
                                  font=("Courier New", 11, "bold"), fg=LEVEL_CLR, bg=BG)
        self.lbl_level.pack(side="right")

        self.canvas = tk.Canvas(root, width=W, height=H, bg=BG,
                                highlightthickness=2, highlightbackground=WALL_COLOR)
        self.canvas.pack(padx=16, pady=(0, 4))

        tk.Label(root, text="WASD / 方向键 移动    P 暂停    R 重开    Q 退出",
                 font=("Courier New", 9), fg=DIM_COLOR, bg=BG).pack(pady=(0, 10))

        root.bind("<KeyPress>", self.on_key)
        root.focus_set()

        self.best = 0
        self.after_id = None
        self._init_game()
        self._draw_grid()
        self._update()

    def _init_game(self):
        cx, cy = COLS // 2, ROWS // 2
        self.snake = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]
        self.snake_set = set(self.snake)
        self.dir = RIGHT
        self.next_dir = RIGHT
        self.score = 0
        self.level = 1
        self.paused = False
        self.over = False
        self.food = self._place_food()
        self._refresh_labels()

    def _place_food(self):
        while True:
            pos = (random.randint(0, COLS - 1), random.randint(0, ROWS - 1))
            if pos not in self.snake_set:
                return pos

    def _speed(self):
        return max(FPS_MIN, FPS_BASE - (self.level - 1) * 8)

    def _refresh_labels(self):
        self.lbl_score.config(text=f"SCORE  {self.score}")
        self.lbl_best.config(text=f"BEST  {self.best}")
        self.lbl_level.config(text=f"LV {self.level}")

    def on_key(self, e):
        k = e.keysym.lower()
        if k == 'q':
            self.root.destroy(); return
        if k == 'r':
            if self.after_id:
                self.root.after_cancel(self.after_id)
            self._init_game()
            self._draw_grid()
            self._update()
            return
        if k == 'p' and not self.over:
            self.paused = not self.paused
            if not self.paused:
                self._update()
            else:
                self._draw()
            return
        dir_map = {
            'up': UP, 'w': UP, 'down': DOWN, 's': DOWN,
            'left': LEFT, 'a': LEFT, 'right': RIGHT, 'd': RIGHT,
        }
        if k in dir_map:
            nd = dir_map[k]
            if nd != OPPOSITE.get(self.dir):
                self.next_dir = nd

    def _step(self):
        self.dir = self.next_dir
        hx, hy = self.snake[0]
        dx, dy = self.dir
        nx, ny = hx + dx, hy + dy
        if nx < 0 or nx >= COLS or ny < 0 or ny >= ROWS:
            self._end_game(); return
        if (nx, ny) in self.snake_set:
            self._end_game(); return
        self.snake.insert(0, (nx, ny))
        self.snake_set.add((nx, ny))
        if (nx, ny) == self.food:
            self.score += 10 * self.level
            self.level = 1 + self.score // 80
            self.food = self._place_food()
            if self.score > self.best:
                self.best = self.score
            self._refresh_labels()
        else:
            tail = self.snake.pop()
            self.snake_set.discard(tail)

    def _end_game(self):
        self.over = True
        if self.score > self.best:
            self.best = self.score
        self._refresh_labels()
        self._draw()

    def _update(self):
        if self.paused or self.over:
            return
        self._step()
        self._draw()
        if not self.over:
            self.after_id = self.root.after(self._speed(), self._update)

    def _draw_grid(self):
        self.canvas.delete("grid")
        for x in range(0, W, CELL):
            self.canvas.create_line(x, 0, x, H, fill=GRID_COLOR, tags="grid")
        for y in range(0, H, CELL):
            self.canvas.create_line(0, y, W, y, fill=GRID_COLOR, tags="grid")

    def _cell_rect(self, gx, gy, shrink=1):
        x1 = gx * CELL + shrink
        y1 = gy * CELL + shrink
        x2 = x1 + CELL - shrink * 2
        y2 = y1 + CELL - shrink * 2
        return x1, y1, x2, y2

    def _draw(self):
        self.canvas.delete("dynamic")

        # 食物
        fx, fy = self.food
        gx, gy, gx2, gy2 = self._cell_rect(fx, fy, -2)
        self.canvas.create_oval(gx, gy, gx2, gy2, fill=FOOD_GLOW, outline="", tags="dynamic")
        x1, y1, x2, y2 = self._cell_rect(fx, fy, 3)
        self.canvas.create_oval(x1, y1, x2, y2, fill=FOOD_COLOR, outline="", tags="dynamic")

        # 蛇
        n = len(self.snake)
        for i in range(n - 1, -1, -1):
            sx, sy = self.snake[i]
            x1, y1, x2, y2 = self._cell_rect(sx, sy, 1)
            if i == 0:
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=HEAD_COLOR, outline=BG, width=1, tags="dynamic")
                dx, dy = self.dir
                ex = (x1 + x2) // 2 + dx * 4
                ey = (y1 + y2) // 2 + dy * 4
                off = 3
                for ex2, ey2 in [(ex - dy * off, ey + dx * off),
                                  (ex + dy * off, ey - dx * off)]:
                    self.canvas.create_oval(ex2 - 2, ey2 - 2, ex2 + 2, ey2 + 2,
                                            fill=BG, outline="", tags="dynamic")
            else:
                color = BODY_COLOR if i / max(n - 1, 1) < 0.5 else BODY_DARK
                self.canvas.create_rectangle(x1, y1, x2, y2,
                                             fill=color, outline=BG, width=1, tags="dynamic")

        if self.paused:
            self.canvas.create_rectangle(0, 0, W, H, fill=BG, stipple="gray50", tags="dynamic")
            self._ct("⏸  已暂停", -20, LEVEL_CLR, 20, True)
            self._ct("按 P 继续", 20, DIM_COLOR, 12)

        if self.over:
            self.canvas.create_rectangle(0, 0, W, H, fill=BG, stipple="gray50", tags="dynamic")
            self._ct("GAME  OVER", -50, FOOD_COLOR, 24, True)
            self._ct(f"得分  {self.score}", -8, TEXT_COLOR, 14)
            self._ct(f"最高  {self.best}", 26, DIM_COLOR, 12)
            self._ct("R 重新开始   Q 退出", 64, SCORE_CLR, 11)

    def _ct(self, text, dy, color, size=14, bold=False):
        font = ("Courier New", size, "bold" if bold else "normal")
        self.canvas.create_text(W // 2, H // 2 + dy,
                                text=text, fill=color, font=font, tags="dynamic")


if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()