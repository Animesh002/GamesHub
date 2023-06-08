import json
import random
from os import path

import pygame

import settings_tetris, sprites_tetris


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption(settings_tetris.TITLE)
        self.screen = pygame.display.set_mode(settings_tetris.WIN_SIZE)
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.font = pygame.font.Font(settings_tetris.FONT, 40)
        self.pieces = (
            sprites_tetris.S_,
            sprites_tetris.Z_,
            sprites_tetris.I_,
            sprites_tetris.O_,
            sprites_tetris.J_,
            sprites_tetris.L_,
            sprites_tetris.T_,
        )
        self.sfx = {
            sound: pygame.mixer.Sound(path.join(settings_tetris.SFX, f"{sound}.wav"))
            for sound in ("explode", "freeze", "rotate")
        }
        self.sprite_sheet = pygame.image.load(settings_tetris.SPRITE_SHEET).convert()
        self.sprite_sheet_info = json.load(open(settings_tetris.SPRITE_SHEET_INFO))

    def get_image(self, file_name):
        for item in self.sprite_sheet_info["frames"]:
            if item["filename"] == file_name:
                x, y = item["frame"]["x"], item["frame"]["y"]
                width, height = item["frame"]["w"], item["frame"]["h"]
                image = pygame.Surface((width, height))
                image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
                image.convert()
                image.set_colorkey(settings_tetris.BLACK)
                return image

    def new_piece(self):
        piece = random.choice(self.pieces)
        x = settings_tetris.INFO
        y = settings_tetris.BLOCK * 3
        return piece((x, y), self, (self.sprites,))

    def launch_piece(self):
        self.current = self.next
        self.current.move((settings_tetris.BLOCK * 4, settings_tetris.BLOCK * -2))
        self.current.falling = True
        self.next = self.new_piece()

    def stack(self):
        for block in self.current.blocks:
            if block.y < 0:
                continue
            xy = (block.x, block.y)
            column, line = xy[0] // settings_tetris.BLOCK, xy[1] // settings_tetris.BLOCK
            self.grid[line][column] = xy
            self.locked[xy] = block
            block.add((self.sprites,))
        self.sfx["freeze"].play()
        if self.current.rect.top < 0:
            self.game_over()
            return
        self.check_lines()
        self.launch_piece()

    def check_lines(self):
        removed = 0
        for i, line in enumerate(self.grid):
            if all(line):
                for j, xy in enumerate(line):
                    self.locked[xy].kill()
                    self.locked.pop(xy)
                    self.grid[i][j] = 0
                removed += 1
                for k in range(i - 1, -1, -1):
                    if any(self.grid[k]):
                        for ln in range(10):
                            if self.grid[k][ln]:
                                pos = self.grid[k][ln]
                                self.grid[k][ln] = 0
                                block = self.locked.pop(pos)
                                block.y += settings_tetris.BLOCK
                                xy = (block.x, block.y)
                                column = xy[0] // settings_tetris.BLOCK
                                line = xy[1] // settings_tetris.BLOCK
                                self.grid[line][column] = xy
                                self.locked[xy] = block
        if removed:
            self.lines += removed
            self.score += (10 * removed) * removed
            self.level_up()
            self.sfx["explode"].play()

    def level_up(self):
        next_level = 1 + (self.score // 500)
        if self.level < next_level:
            self.level = next_level
            self.speed //= 2

    def game_over(self):
        self.sprites.empty()
        self.splash_screen = sprites_tetris.SplashScreen("GAME OVER", (self.sprites,))

    def info(self):
        x = settings_tetris.INFO
        y = settings_tetris.BLOCK
        self.text("Next", (x, y))
        self.text("Score", (x, y * 6))
        self.text(f"{self.score:0>6}", (x, y * 7))
        self.text("Lines", (x, y * 9))
        self.text(f"{self.lines}", (x, y * 10))
        self.text("Level", (x, y * 12))
        self.text(f"{self.level}", (x, y * 13))

    def reset(self):
        self.sprites.empty()
        self.grid = [[0 for _ in range(10)] for _ in range(20)]
        self.locked = {}
        self.lines = 0
        self.score = 0
        self.level = 1
        self.speed = 1000
        self.next = self.new_piece()
        self.splash_screen = None
        self.launch_piece()

    def start(self):
        self.sprites.empty()
        self.splash_screen = sprites_tetris.SplashScreen(
            settings_tetris.TITLE, (self.sprites,)
        )

    def update(self):
        self.sprites.update()

    def draw(self):
        self.screen.fill(settings_tetris.BLACK)
        self.sprites.draw(self.screen)
        if not self.splash_screen:
            self.info()
            pygame.draw.lines(
                self.screen, settings_tetris.WHITE, True, settings_tetris.BORDER
            )
        pygame.display.flip()

    def text(self, txt, xy):
        surface = self.font.render(txt, True, settings_tetris.WHITE)
        surface_rect = surface.get_rect()
        surface_rect.topleft = xy
        self.screen.blit(surface, surface_rect)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if self.splash_screen:
                    self.reset()
                    return
                if event.key == pygame.K_a:
                    self.current.left()
                if event.key == pygame.K_d:
                    self.current.right()
                if event.key == pygame.K_s:
                    self.current.down()
                if event.key == pygame.K_w:
                    self.current.rotate()
                if event.key == pygame.K_SPACE:
                    self.current.drop()

    def loop(self):
        while self.running:
            self.clock.tick(settings_tetris.FPS)
            self.update()
            self.draw()
            self.events()

    def run(self):
        self.running = True
        self.start()
        self.loop()
        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
