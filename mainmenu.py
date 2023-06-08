import pygame
import os
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Games Vault")
font = pygame.font.Font(None, 50)
play_button = font.render("PLAY", True, (255, 153, 51))
play_button_rect = play_button.get_rect(center=(screen_width//2, screen_height//2-50))
quit_button = font.render("QUIT", True, (255, 153, 51))
quit_button_rect = quit_button.get_rect(center=(screen_width//2, screen_height//2+50))

def next_screen():
    TILE_SIZE = 250
    SCREEN_WIDTH = 1000
    SCREEN_HEIGHT = 500
    # Define the colors to use for the tiles
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (255, 0, 255)
    CYAN = (0, 255, 255)

    # Define the games to launch when the tiles are clicked
    GAMES = [
        {'name': 'JUMPING FROG', 'command': 'f1.py'},
        {'name': 'MARIO REMAKE', 'command': 'main_marioremake.py'},
        {'name': 'SPACE SHOOTER', 'command': 'SpaceShooter.py'},
        {'name': 'PAC-MAN REMAKE', 'command': 'pacman.py'},
        {'name': 'CLASSIC SNAKE GAME', 'command': 'SnakeGame.py'},
        {'name': '2048 GAME', 'command': '2048.py'},
        {'name': 'TARGET SHOOTER GAME', 'command': 'main_shooter.py'},
        {'name': 'TETRIS REMASTERED', 'command': 'game_tetris.py'},

    ]

    # Define the font to use for the tile labels
    FONT = pygame.font.SysFont("Arial", 20)

    # Create the Pygame window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Game Software")

    # Set the background color of the Pygame window
    background_color = pygame.image.load('assets/bg_itachi.png').convert_alpha()

    # Define a function to draw a tile
    def draw_tile(x, y, color, label):
        rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, color, rect, 0)
        label_text = FONT.render(label, True, (0, 0, 0))
        label_rect = label_text.get_rect()
        label_rect.center = rect.center
        screen.blit(label_text, label_rect)

    # Define a function to launch a game
    def launch_game(command):
        os.system(command)

    # Define a function to display the game menu
    def display_menu():
        # Clear the screen
        screen.blit(background_color,(0,0))

        # Draw the tiles
        tiles_per_row = SCREEN_WIDTH // TILE_SIZE
        for i in range(len(GAMES)):
            x = (i % tiles_per_row) * TILE_SIZE
            y = (i // tiles_per_row) * TILE_SIZE
            color = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN][i % 6]
            draw_tile(x, y, color, GAMES[i]['name'])

        # Update the display
        pygame.display.flip()

    # Display the game menu
    display_menu()

    # Run the game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                x, y = pygame.mouse.get_pos()

                # Calculate the index of the tile that was clicked
                tile_x = x // TILE_SIZE
                tile_y = y // TILE_SIZE
                tile_index = tile_x + tile_y * (SCREEN_WIDTH // TILE_SIZE)

                # If a valid tile was clicked, launch the corresponding game
                if tile_index < len(GAMES):
                    launch_game(GAMES[tile_index]['command'])
                    display_menu()
    pygame.display.update()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_pos):
                # code to start the game
                next_screen()
            elif quit_button_rect.collidepoint(mouse_pos):
                pygame.quit()
                quit()

    image_front = pygame.image.load('assets/front.png').convert_alpha()
    screen.blit(image_front,(0,0))

    # Draw the buttons
    screen.blit(play_button, play_button_rect)
    screen.blit(quit_button, quit_button_rect)

    pygame.display.update()
