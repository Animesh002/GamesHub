import pygame

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Define colors
BLACK = (0, 0, 0)

# Create the window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Menu")

# Load the images
tile1 = pygame.image.load("assets/bg_itachi.png").convert_alpha()
tile2 = pygame.image.load("assets/front.png").convert_alpha()

# Resize the images to the desired size
tile1 = pygame.transform.scale(tile1, (200, 200))
tile2 = pygame.transform.scale(tile2, (200, 200))

# Define the rectangles for the tiles
tile1_rect = tile1.get_rect(center=(SCREEN_WIDTH//4, SCREEN_HEIGHT//2))
tile2_rect = tile2.get_rect(center=(3*SCREEN_WIDTH//4, SCREEN_HEIGHT//2))

# Define the main menu function
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if tile1_rect.collidepoint(mouse_pos):
                    print("Tile 1 clicked")
                elif tile2_rect.collidepoint(mouse_pos):
                    print("Tile 2 clicked")

        # Draw the tiles on the screen
        screen.fill(BLACK)
        screen.blit(tile1, tile1_rect)
        screen.blit(tile2, tile2_rect)

        # Update the display
        pygame.display.update()

# Start the game
main_menu()