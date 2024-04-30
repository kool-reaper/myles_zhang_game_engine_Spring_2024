import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define colors with alpha (R, G, B, Alpha)
SEMI_TRANSPARENT_COLOR = (255, 0, 0, 128)  # Red with 50% transparency

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill((255, 255, 255))

    # Create a semi-transparent surface
    transparent_surface = pygame.Surface((200, 150), pygame.SRCALPHA)
    transparent_surface.fill(SEMI_TRANSPARENT_COLOR)

    # Position where the transparent box will be blitted
    position = (300, 200)

    # Blit the semi-transparent surface onto the main screen
    screen.blit(transparent_surface, position)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
