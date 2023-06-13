import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH, HEIGHT = 640, 480
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Define the Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.positions = [(random.randint(0, WIDTH // 20) * 20, random.randint(0, HEIGHT // 20) * 20)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move(self):
        x, y = self.positions[0]
        if self.direction == "UP":
            y -= 20
        elif self.direction == "DOWN":
            y += 20
        elif self.direction == "LEFT":
            x -= 20
        elif self.direction == "RIGHT":
            x += 20
        self.positions.insert(0, (x, y))
        if len(self.positions) > self.size:
            self.positions.pop()

    def change_direction(self, new_direction):
        if new_direction == "UP" and self.direction != "DOWN":
            self.direction = new_direction
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = new_direction
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = new_direction
        elif new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = new_direction

    def draw(self):
        for position in self.positions:
            pygame.draw.rect(WIN, GREEN, (position[0], position[1], 20, 20))

# Define the Fruit class
class Fruit:
    def __init__(self):
        self.position = (random.randint(0, WIDTH // 20 - 1) * 20, random.randint(0, HEIGHT // 20 - 1) * 20)

    def draw(self):
        pygame.draw.rect(WIN, RED, (self.position[0], self.position[1], 20, 20))

# Define the Scoreboard class
class Scoreboard:
    def __init__(self):
        self.score = 0
        self.font = pygame.font.SysFont(None, 30)

    def update(self):
        self.score += 1

    def draw(self):
        text = self.font.render("Score: " + str(self.score), True, WHITE)
        WIN.blit(text, (10, 10))

# Initialize the Snake, Fruit, and Scoreboard objects
snake = Snake()
fruit = Fruit()
scoreboard = Scoreboard()

clock = pygame.time.Clock()

# Game loop
running = True
game_over = False
while running:
    clock.tick(10)  # Adjust snake speed here

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

    # Move the snake
    if not game_over:
        snake.move()

        # Check for collision with fruit
        if snake.positions[0] == fruit.position:
            snake.size += 1
            scoreboard.update()
            fruit = Fruit()

        # Check for collision with the edges of the window
        if (
            snake.positions[0][0] < 0
            or snake.positions[0][0] >= WIDTH
            or snake.positions[0][1] < 0
            or snake.positions[0][1] >= HEIGHT
        ):
            game_over = True

        # Check for collision with the snake's own body
        if snake.positions[0] in snake.positions[1:]:
            game_over = True

    # Clear the window
    WIN.fill(BLACK)

    # Draw the snake, fruit, and scoreboard
    snake.draw()
    fruit.draw()
    scoreboard.draw()

    # Show game over screen
    if game_over:
        text = scoreboard.font.render("Game Over!", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        WIN.blit(text, text_rect)

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
