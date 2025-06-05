# === File: tetris/main.py ===
import pygame
import random
import sys

# Constants
WIDTH, HEIGHT = 300, 600
ROWS, COLS = 20, 10
CELL_SIZE = WIDTH // COLS
FPS = 60

# Colors
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255), (0, 0, 255), (255, 165, 0),
    (255, 255, 0), (0, 255, 0), (128, 0, 128), (255, 0, 0)
]

# Shapes (Tetriminos)
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]]
}

# Initialize
pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Grid
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

# Shape class
class Shape:
    def __init__(self):
        self.type = random.choice(list(SHAPES.keys()))
        self.color = random.choice(COLORS)
        self.shape = SHAPES[self.type]
        self.row = 0
        self.col = COLS // 2 - len(self.shape[0]) // 2

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def collision(self, dx=0, dy=0):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.col + x + dx
                    new_y = self.row + y + dy
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS or (new_y >= 0 and grid[new_y][new_x]):
                        return True
        return False

    def lock(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and self.row + y >= 0:
                    grid[self.row + y][self.col + x] = self.color

    def draw(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(win, self.color,
                        (CELL_SIZE * (self.col + x), CELL_SIZE * (self.row + y), CELL_SIZE, CELL_SIZE))

# Line clearing
def clear_lines():
    global grid
    grid = [row for row in grid if any(cell == 0 for cell in row)]
    while len(grid) < ROWS:
        grid.insert(0, [0 for _ in range(COLS)])

# Draw grid
def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            cell = grid[y][x]
            if cell:
                pygame.draw.rect(win, cell, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(win, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Main
current = Shape()
drop_time = 0
speed = 500  # ms

while True:
    win.fill(BLACK)
    clock.tick(FPS)
    drop_time += clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not current.collision(dx=-1):
                current.col -= 1
            if event.key == pygame.K_RIGHT and not current.collision(dx=1):
                current.col += 1
            if event.key == pygame.K_DOWN and not current.collision(dy=1):
                current.row += 1
            if event.key == pygame.K_UP:
                current.rotate()
                if current.collision():
                    for _ in range(3): current.rotate()  # rotate back

    if drop_time > speed:
        if not current.collision(dy=1):
            current.row += 1
        else:
            current.lock()
            clear_lines()
            current = Shape()
            if current.collision():
                print("Game Over")
                pygame.quit()
                sys.exit()
        drop_time = 0

    draw_grid()
    current.draw()
    pygame.display.update()
