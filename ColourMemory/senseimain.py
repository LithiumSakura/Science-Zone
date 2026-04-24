import pygame
import random
import sys

pygame.init()

# Screen setup
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Color Memory Match")
clock = pygame.time.Clock()

# Colors
FROST = (255, 224, 233) # Petal Frost
MAUVE = (82, 46, 56) # Mauve Shadow
PLUM = (96, 36, 55) # Wine Plum
ROSE = (185, 55, 94) # Rosewood
BLUSH = (224, 87, 128) # Blush Rose
PETAL = (255, 122, 162) # Petal Rouge
BLOSSOM = (255, 194, 212) # Soft Blossom
WINE = (138, 40, 70) # Dark Amaranth
MIST = (255, 158, 187) # Pink Mist

# Fonts
big_font = pygame.font.Font(None, 72)
font = pygame.font.Font(None, 48)
small_font = pygame.font.Font(None, 36)

# Game colors to remember
GAME_COLORS = [ROSE, BLUSH, PETAL, BLOSSOM, WINE, MIST]

# Game state
game_state = "start"  # start, show, memorize, playing, correct, wrong, win
sequence = []
player_sequence = []
level = 1
score = 0

# Create colored squares (4x4 grid)
squares = []
for row in range(4):
    for col in range(4):
        # Only use 6 squares (3 pairs)
        if len(squares) < 6:
            x = 150 + col * 130
            y = 150 + row * 130
            # Add each color twice for matching pairs
            if len(squares) < 3:
                squares.append({"x": x, "y": y, "color": GAME_COLORS[len(squares)], "clicked": False})
            else:
                squares.append({"x": x, "y": y, "color": GAME_COLORS[len(squares) - 3], "clicked": False})

# Shuffle squares
random.shuffle(squares)

# Selected squares for matching
selected = []
show_timer = 0
wait_timer = 0

# MAIN GAME LOOP
running = True
while running:
    dt = clock.tick(60) / 1000.0
    
    # EVENT HANDLING
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Start screen
        if event.type == pygame.KEYDOWN and game_state == "start":
            if event.key == pygame.K_SPACE:
                game_state = "playing"
        
        # Playing - click squares
        if event.type == pygame.MOUSEBUTTONDOWN and game_state == "playing":
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check which square was clicked
            for square in squares:
                if not square["clicked"]:
                    # Check if mouse is inside square
                    if (square["x"] <= mouse_x <= square["x"] + 100 and
                        square["y"] <= mouse_y <= square["y"] + 100):
                        
                        # Add to selected if not already selected
                        if square not in selected:
                            selected.append(square)
                            
                            # If 2 squares selected, check if they match
                            if len(selected) == 2:
                                if selected[0]["color"] == selected[1]["color"]:
                                    # Match!
                                    selected[0]["clicked"] = True
                                    selected[1]["clicked"] = True
                                    score += 10
                                    game_state = "correct"
                                    show_timer = 0.5
                                else:
                                    # No match
                                    game_state = "wrong"
                                    show_timer = 1.0
        
        # Restart
        if event.type == pygame.KEYDOWN and game_state == "win":
            if event.key == pygame.K_r:
                # Reset everything
                game_state = "start"
                score = 0
                selected = []
                for square in squares:
                    square["clicked"] = False
                random.shuffle(squares)
    
    # GAME LOGIC
    if game_state == "correct" or game_state == "wrong":
        show_timer -= dt
        if show_timer <= 0:
            selected = []
            game_state = "playing"
            
            # Check if all squares matched
            all_matched = True
            for square in squares:
                if not square["clicked"]:
                    all_matched = False
            
            if all_matched:
                game_state = "win"
    
    # DRAW EVERYTHING
    screen.fill(MAUVE)
    
    # Draw title
    title = font.render("Color Memory Match", True, FROST)
    screen.blit(title, (WIDTH // 2 - 200, 20))
    
    # Draw score
    score_text = small_font.render(f"Score: {score}", True, BLOSSOM)
    screen.blit(score_text, (20, 20))
    
    # Start screen
    if game_state == "start":
        instructions = [
            "Match all the colored pairs!",
            "",
            "Click two squares to flip them",
            "Match all pairs to win!",
            "",
            "Press SPACE to start"
        ]
        
        y = 200
        for line in instructions:
            text = small_font.render(line, True, FROST)
            screen.blit(text, (WIDTH // 2 - 200, y))
            y += 50
    
    # Playing - draw squares
    elif game_state in ["playing", "correct", "wrong"]:
        for square in squares:
            # Show color if clicked or selected
            if square["clicked"] or square in selected:
                pygame.draw.rect(screen, square["color"], 
                               (square["x"], square["y"], 100, 100))
            else:
                # Show gray back
                pygame.draw.rect(screen, PLUM, 
                               (square["x"], square["y"], 100, 100))
            
            # White border
            pygame.draw.rect(screen, FROST, 
                           (square["x"], square["y"], 100, 100), 3)
        
        # Show feedback
        if game_state == "correct":
            feedback = font.render("MATCH!", True, BLUSH)
            screen.blit(feedback, (WIDTH // 2 - 80, HEIGHT - 80))
        elif game_state == "wrong":
            feedback = font.render("Try Again!", True, ROSE)
            screen.blit(feedback, (WIDTH // 2 - 120, HEIGHT - 80))
    
    # Win screen
    elif game_state == "win":
        win_text = big_font.render("YOU WIN!", True, BLUSH)
        final_score = font.render(f"Final Score: {score}", True, FROST)
        restart = small_font.render("Press R to play again", True, FROST)
        
        screen.blit(win_text, (WIDTH // 2 - 150, HEIGHT // 2 - 100))
        screen.blit(final_score, (WIDTH // 2 - 150, HEIGHT // 2 - 20))
        screen.blit(restart, (WIDTH // 2 - 150, HEIGHT // 2 + 40))
    
    pygame.display.flip()

pygame.quit()
sys.exit()
