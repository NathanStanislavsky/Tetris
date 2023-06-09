import pygame
import random
import time

class Block:
    def __init__(self):
        self.block = random.randint(1, 7)
        self.color = self.get_color()
        self.x = board_width // 2
        self.y = 0
        self.last_fall_time = time.time()
        self.block_shape = self.create_block()

    def get_color(self):
        colors = {
            1: (0, 255, 255),   # Cyan
            2: (255, 255, 0),   # Yellow
            3: (128, 0, 128),   # Purple
            4: (0, 255, 0),     # Green
            5: (255, 0, 0),     # Red
            6: (0, 0, 255),     # Blue
            7: (255, 127, 0)    # Orange
        }
        return colors[self.block]

    def create_block(self):
        if self.block == 1:
            return [[1, 1, 1, 1]]
        elif self.block == 2:
            return [[1, 1], [1, 1]]
        elif self.block == 3:
            return [[1, 1, 1], [0, 1, 0]]
        elif self.block == 4:
            return [[1, 1, 0], [0, 1, 1]]
        elif self.block == 5:
            return [[0, 1, 1], [1, 1, 0]]
        elif self.block == 6:
            return [[1, 1, 1], [1, 0, 0]]
        elif self.block == 7:
            return [[1, 1, 1], [0, 0, 1]]

    def update_position(self):
        if time.time() - self.last_fall_time > 1:  # 1 second delay for each move
            if self.check_collision(self.x, self.y + 1):
                self.y += 1
                self.last_fall_time = time.time()
            else:
                self.lock_block()
                self.y = 0
                self.x = board_width // 2
                self.block = random.randint(1, 7)
                self.color = self.get_color()
                self.block_shape = self.create_block()

    def check_collision(self, x, y, block_shape=None):
        if block_shape is None:
            block_shape = self.create_block()
        for r in range(len(block_shape)):
            for c in range(len(block_shape[r])):
                if block_shape[r][c] == 1:
                    if (
                        x + c < 0
                        or x + c >= board_width
                        or y + r >= board_height
                        or y + r < 0
                        or board[y + r][x + c] != 0
                    ):
                        return False
        return True

    def lock_block(self):
        for r in range(len(self.block_shape)):
            for c in range(len(self.block_shape[r])):
                if self.block_shape[r][c] == 1:
                    board[self.y + r][self.x + c] = self.block

    def rotate_block_clockwise(self):
        rotated_block = list(zip(*reversed(self.block_shape)))
        if self.check_collision(self.x, self.y, rotated_block):
            # Clear previous block shape from the board
            for r in range(len(self.block_shape)):
                for c in range(len(self.block_shape[r])):
                    if self.block_shape[r][c] == 1:
                        board[self.y + r][self.x + c] = 0
            self.block_shape = rotated_block

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
cell_size = 30
board_width = 10
board_height = 20

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the board
board = [[0 for _ in range(board_width)] for _ in range(board_height)]

# Create a block
current_block = Block()

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if current_block.check_collision(current_block.x - 1, current_block.y):
                    current_block.x -= 1
            elif event.key == pygame.K_RIGHT:
                if current_block.check_collision(current_block.x + 1, current_block.y):
                    current_block.x += 1
            elif event.key == pygame.K_DOWN:
                if current_block.check_collision(current_block.x, current_block.y + 1):
                    current_block.y += 1
            elif event.key == pygame.K_UP:
                current_block.rotate_block_clockwise()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the board
    for r in range(board_height):
        for c in range(board_width):
            pygame.draw.rect(screen, WHITE, (c * cell_size, r * cell_size, cell_size, cell_size))

    # Update the position of the current block
    current_block.update_position()

    # Create and draw the current block
    block_shape = current_block.block_shape
    for r in range(len(block_shape)):
        for c in range(len(block_shape[r])):
            if block_shape[r][c] == 1:
                pygame.draw.rect(screen, current_block.color, ((current_block.x + c) * cell_size, (current_block.y + r) * cell_size, cell_size, cell_size))

    # Update the board with locked blocks
    for r in range(board_height):
        for c in range(board_width):
            if board[r][c] != 0:
                pygame.draw.rect(screen, current_block.get_color(), (c * cell_size, r * cell_size, cell_size, cell_size))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
