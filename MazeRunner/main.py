import pygame
import random
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
CELL_SIZE = 40

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
PURPLE = (138, 43, 226)
ORANGE = (255, 140, 0)
GRAY = (70, 70, 70)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Runner")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

class Player:
    def __init__(self, x, y, offset_x, offset_y):
        self.grid_x = x
        self.grid_y = y
        self.x = x * CELL_SIZE + CELL_SIZE // 2 + offset_x
        self.y = y * CELL_SIZE + CELL_SIZE // 2 + offset_y
        self.size = CELL_SIZE - 10
        self.speed = 3
        self.color = BLUE
        self.offset_x = offset_x
        self.offset_y = offset_y
        
    def move(self, dx, dy, maze):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        grid_x = int((new_x - self.offset_x) / CELL_SIZE)
        grid_y = int((new_y - self.offset_y) / CELL_SIZE)
        
        if grid_x < 0 or grid_x >= len(maze[0]) or grid_y < 0 or grid_y >= len(maze):
            return
        
        if maze[grid_y][grid_x] == 0:
            self.x = new_x
            self.y = new_y
            
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size // 2)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size // 2, 2)

class Coin:
    def __init__(self, x, y, offset_x, offset_y):
        self.x = x * CELL_SIZE + CELL_SIZE // 2 + offset_x
        self.y = y * CELL_SIZE + CELL_SIZE // 2 + offset_y
        self.collected = False
        self.size = 12
        
    def draw(self):
        if not self.collected:
            pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.size)
            pygame.draw.circle(screen, ORANGE, (self.x, self.y), self.size - 3)

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve(x, y):
        maze[y][x] = 0
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0
                carve(nx, ny)
    
    carve(1, 1)
    return maze

def place_coins(maze, num_coins, offset_x, offset_y):
    coins = []
    empty_cells = []
    
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 0 and not (x == 1 and y == 1):
                empty_cells.append((x, y))
    
    random.shuffle(empty_cells)
    for i in range(min(num_coins, len(empty_cells))):
        x, y = empty_cells[i]
        coins.append(Coin(x, y, offset_x, offset_y))
    
    return coins

def draw_maze(maze, offset_x, offset_y):
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:
                pygame.draw.rect(screen, GRAY, 
                               (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y, 
                                CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, WHITE, 
                               (x * CELL_SIZE + offset_x, y * CELL_SIZE + offset_y, 
                                CELL_SIZE, CELL_SIZE), 1)

def main():
    # Generate maze
    maze_width = 15
    maze_height = 12
    maze = generate_maze(maze_width, maze_height)
    
    offset_x = (WIDTH - maze_width * CELL_SIZE) // 2
    offset_y = 80
    
    # Player starts at top-left open area
    player = Player(1, 1, offset_x, offset_y)
    
    # Find bottom-right open area for goal
    goal_x = (maze_width - 2) * CELL_SIZE + CELL_SIZE // 2 + offset_x
    goal_y = (maze_height - 2) * CELL_SIZE + CELL_SIZE // 2 + offset_y
    
    # Place coins
    coins = place_coins(maze, 10, offset_x, offset_y)
    
    score = 0
    time_elapsed = 0
    level = 1
    game_won = False
    
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_won:
                    # Next level
                    level += 1
                    maze = generate_maze(maze_width, maze_height)
                    player = Player(1, 1, offset_x, offset_y)
                    coins = place_coins(maze, 10 + level, offset_x, offset_y)
                    time_elapsed = 0
                    game_won = False
                elif event.key == pygame.K_r:
                    # Restart current level
                    player = Player(1, 1, offset_x, offset_y)
                    time_elapsed = 0
        
        if not game_won:
            time_elapsed += dt
            
            # Player movement
            keys = pygame.key.get_pressed()
            dx = dy = 0
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                dx = 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                dy = -1
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                dy = 1
            
            if dx != 0 or dy != 0:
                player.move(dx, dy, maze)
            
            # Check coin collection
            for coin in coins:
                if not coin.collected:
                    dist = ((player.x - coin.x) ** 2 + (player.y - coin.y) ** 2) ** 0.5
                    if dist < player.size // 2 + coin.size:
                        coin.collected = True
                        score += 100
            
            # Check if reached goal
            dist_to_goal = ((player.x - goal_x) ** 2 + (player.y - goal_y) ** 2) ** 0.5
            if dist_to_goal < CELL_SIZE // 2:
                game_won = True
                score += max(0, int(1000 - time_elapsed * 10))
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw maze
        draw_maze(maze, offset_x, offset_y)
        
        # Draw goal
        pygame.draw.circle(screen, GREEN, (int(goal_x), int(goal_y)), CELL_SIZE // 3)
        pygame.draw.circle(screen, WHITE, (int(goal_x), int(goal_y)), CELL_SIZE // 3, 2)
        
        # Draw coins
        for coin in coins:
            coin.draw()
        
        # Draw player
        player.draw()
        
        # Draw UI
        score_text = font.render(f"Score: {score}", True, WHITE)
        time_text = font.render(f"Time: {int(time_elapsed)}s", True, WHITE)
        level_text = font.render(f"Level: {level}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(time_text, (WIDTH // 2 - 60, 10))
        screen.blit(level_text, (WIDTH - 150, 10))
        
        # Instructions
        inst_text = small_font.render("WASD/Arrows to move | R to restart", True, GRAY)
        screen.blit(inst_text, (WIDTH // 2 - 160, HEIGHT - 30))
        
        # Win message
        if game_won:
            win_text = font.render("LEVEL COMPLETE!", True, GREEN)
            continue_text = small_font.render("Press SPACE for next level", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - 130, HEIGHT // 2 - 40))
            screen.blit(continue_text, (WIDTH // 2 - 130, HEIGHT // 2))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
