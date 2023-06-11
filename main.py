import pygame
import random
import time

score = 0

class Block:
    def __init__(self):
        self.block = random.randint(1, 7)
        self.color = self.get_color()
        self.x = board_width // 2
        self.y = 0
        self.fall_speed = 1.0
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
        
    def fall(self):
        if time.time() - self.last_fall_time >= self.fall_speed:
            if self.check_collision(self.x, self.y + 1):
                self.y += 1
            else:
                self.freeze()  # The block cannot fall further, freeze it on the board
                self.clear_lines()  # Check if any lines are complete and clear them if necessary
                self.spawn_new_block()  # Spawn a new block
            self.last_fall_time = time.time()

    def freeze(self):
        # Update the board with the current block's shape and color
        for r in range(len(self.block_shape)):
            for c in range(len(self.block_shape[r])):
                if self.block_shape[r][c] == 1:
                    board[self.y + r][self.x + c] = self.color

    def clear_lines(self):
        global score
        line_count = 0
        lines_to_clear = []
        for r in range(board_height):
            if all(board[r]):
                lines_to_clear.append(r)

        for line in lines_to_clear:
            line_count += 1

        if line_count == 1:
            score += 40
        elif line_count == 2:
            score += 100
        elif line_count == 3:
            score += 300
        elif line_count == 4:
            score += 800
        else:
            score += 0

        # Clear the complete lines
        for line in lines_to_clear:
            del board[line]
            board.insert(0, [0 for _ in range(board_width)])


    def spawn_new_block(self):
        global current_block
        global next_block
        current_block = next_block
        next_block = Block()

    def move(self, direction):
        global score
        # left
        if direction == 1 and self.check_collision(self.x - 1, self.y):
            self.x -= 1

        # right
        if direction == 2 and self.check_collision(self.x + 1, self.y):
            self.x += 1
        
        # down
        if direction == 3 and self.check_collision(self.x, self.y + 1):
            score += 1 # points awarded per cell dropped
            self.y += 1
            
        # rotate clockwise
        if direction == 4:
            # Transpose the block shape matrix
            transposed_shape = [[self.block_shape[j][i] for j in range(len(self.block_shape))] for i in range(len(self.block_shape[0]))]
            # Reverse each row of the transposed matrix to achieve clockwise rotation
            rotated_shape = [row[::-1] for row in transposed_shape]
            # Check collision for the rotated shape
            if self.check_collision(self.x, self.y, rotated_shape):
                # Update the block shape
                self.block_shape = rotated_shape
                # Adjust the position if the rotated block goes out of bounds
                if self.x + len(self.block_shape[0]) > board_width:
                    self.x = board_width - len(self.block_shape[0])
                if self.y + len(self.block_shape) > board_height:
                    self.y = board_height - len(self.block_shape)

        
        if direction == 5:
            while self.check_collision(self.x, self.y + 1):
                score += 5 # points awarded per cell dropped
                self.y += 1
            self.freeze()
            self.clear_lines()
            self.spawn_new_block()

    def check_collision(self, x, y, shape=None):
        if shape is None:
            shape = self.block_shape
        for r in range(len(shape)):
            for c in range(len(shape[r])):
                if shape[r][c] == 1:
                    if (
                        x + c < 0
                        or x + c >= board_width
                        or y + r >= board_height
                        or y + r < 0
                        or board[y + r][x + c] != 0
                    ):
                        return False
        return True

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 600
cell_size = 30
board_width = 10
board_height = 20

preview_width = 6  # Adjust the width of the preview section
preview_height = 4  # Adjust the height of the preview section

# Calculate the dimensions and position of the preview section
preview_x = board_width + 2
preview_y = 4
preview_cell_size = 30

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Tetris")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize the board
board = [[0 for _ in range(board_width)] for _ in range(board_height)]

# Initialize preview section
preview_section = [[0 for _ in range(preview_width)] for _ in range(preview_height)]

# Create a block
current_block = Block()
next_block = Block()

# Game loop
running = True
move_left = False
move_right = False
move_down = False
last_move_time = time.time()
move_delay = 0.1  # Adjust this value to control the movement speed

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_left = True
            elif event.key == pygame.K_RIGHT:
                move_right = True
            elif event.key == pygame.K_DOWN:
                move_down = True
            elif event.key == pygame.K_UP:
                current_block.move(4)
            elif event.key == pygame.K_SPACE:  
                current_block.move(5)  # Trigger hard drop
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                move_left = False
            elif event.key == pygame.K_RIGHT:
                move_right = False
            elif event.key == pygame.K_DOWN:
                move_down = False
    
    # Movement logic
    if move_left and time.time() - last_move_time >= move_delay:
        current_block.move(1)
        last_move_time = time.time()
    if move_right and time.time() - last_move_time >= move_delay:
        current_block.move(2)
        last_move_time = time.time()
    if move_down and time.time() - last_move_time >= move_delay:
        current_block.move(3)
        last_move_time = time.time()

    current_block.fall()

    # Clear the screen
    screen.fill(BLACK)

    # Draw the board
    for r in range(board_height):
        for c in range(board_width):
            pygame.draw.rect(screen, WHITE, (c * cell_size, r * cell_size, cell_size, cell_size))
            if board[r][c] != 0:
                pygame.draw.rect(screen, board[r][c], (c * cell_size, r * cell_size, cell_size, cell_size))

    # Create and draw the current block
    block_shape = current_block.block_shape
    for r in range(len(block_shape)):
        for c in range(len(block_shape[r])):
            if block_shape[r][c] == 1:
                block_x = current_block.x + c
                block_y = current_block.y + r

                pygame.draw.rect(screen, current_block.color, (block_x * cell_size, block_y * cell_size, cell_size, cell_size))

    # Render and display the score
    score_text = pygame.font.Font(None, 36).render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (350, 20))

    # Display next block
    preview_text = pygame.font.Font(None, 24).render("Next Block:", True, WHITE)
    screen.blit(preview_text, (350, 70))

    next_block_shape = next_block.block_shape
    for r in range(len(next_block_shape)):
        for c in range(len(next_block_shape[r])):
            if next_block_shape[r][c] == 1:
                block_x = preview_x + c
                block_y = preview_y + r

                pygame.draw.rect(screen, next_block.color, (block_x * preview_cell_size, block_y * preview_cell_size, preview_cell_size, preview_cell_size))

    # Update the display
    pygame.display.flip()


# Quit the game
pygame.quit()

