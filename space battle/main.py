import pygame
import os
from pymagic.my_library import MagicEffects, FireballEffect, ExplosionEffect

# Constants
WIDTH, HEIGHT = 900, 500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

pygame.font.init()
pygame.mixer.init()

# Window setup
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Battle!")

# Fonts
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Load images
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Sounds
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))

# Effects
magic = MagicEffects(WIN)
fireball_effect = FireballEffect(WIN)
explosion_effect = ExplosionEffect(WIN)

class Spaceship:
    def __init__(self, x, y, image, controls, left_bound, right_bound):
        self.rect = pygame.Rect(x, y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
        self.image = image
        self.controls = controls
        self.left_bound = left_bound
        self.right_bound = right_bound
        self.health = 10
        self.bullets = []

    def draw(self):
        WIN.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            pygame.draw.rect(WIN, RED if self.image == RED_SPACESHIP else YELLOW, bullet)

    def move(self, keys_pressed):
        if keys_pressed[self.controls['left']] and self.rect.x - VEL > self.left_bound:
            self.rect.x -= VEL
        if keys_pressed[self.controls['right']] and self.rect.x + VEL + self.rect.width < self.right_bound:
            self.rect.x += VEL
        if keys_pressed[self.controls['up']] and self.rect.y - VEL > 0:
            self.rect.y -= VEL
        if keys_pressed[self.controls['down']] and self.rect.y + VEL + self.rect.height < HEIGHT - 15:
            self.rect.y += VEL

    def shoot(self, direction):
        if len(self.bullets) < MAX_BULLETS:
            bullet = pygame.Rect(
                self.rect.x + (self.rect.width if direction > 0 else -10),
                self.rect.y + self.rect.height // 2 - 2,
                10, 5
            )
            self.bullets.append(bullet)
            BULLET_FIRE_SOUND.play()

class Game:
    def __init__(self):
        self.border = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)
        self.red = Spaceship(700, 300, RED_SPACESHIP,
                             {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,
                              'up': pygame.K_UP, 'down': pygame.K_DOWN,
                              'shoot': pygame.K_RCTRL},
                             self.border.x + self.border.width, WIDTH)
        self.yellow = Spaceship(100, 300, YELLOW_SPACESHIP,
                                {'left': pygame.K_a, 'right': pygame.K_d,
                                 'up': pygame.K_w, 'down': pygame.K_s,
                                 'shoot': pygame.K_LCTRL},
                                0, self.border.x)

    def draw_window(self):
        WIN.blit(SPACE, (0, 0))
        pygame.draw.rect(WIN, BLACK, self.border)

        red_health_text = HEALTH_FONT.render("Health: " + str(self.red.health), 1, WHITE)
        yellow_health_text = HEALTH_FONT.render("Health: " + str(self.yellow.health), 1, WHITE)
        WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
        WIN.blit(yellow_health_text, (10, 10))

        self.red.draw()
        self.yellow.draw()

        pygame.display.update()

    def handle_bullets(self):
        for bullet in self.yellow.bullets[:]:
            bullet.x += BULLET_VEL
            if self.red.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(RED_HIT))
                self.yellow.bullets.remove(bullet)
                explosion_effect.create_explosion(self.red.rect.x, self.red.rect.y)
                pygame.display.update()
                pygame.time.delay(50)
            elif bullet.x > WIDTH:
                self.yellow.bullets.remove(bullet)

        for bullet in self.red.bullets[:]:
            bullet.x -= BULLET_VEL
            if self.yellow.rect.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT))
                self.red.bullets.remove(bullet)
                explosion_effect.create_explosion(self.yellow.rect.x, self.yellow.rect.y)
                pygame.display.update()
                pygame.time.delay(50)
            elif bullet.x < 0:
                self.red.bullets.remove(bullet)

    def draw_winner(self, text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
        restart_text = HEALTH_FONT.render("Taper R pour rejouer", 1, WHITE)
        WIN.blit(restart_text, (WIDTH / 2 - restart_text.get_width() / 2, HEIGHT / 2 + 60))
        pygame.display.update()

    def draw_menu(self):
        title_font = pygame.font.SysFont('comicsans', 60)
        menu_font = pygame.font.SysFont('comicsans', 40)

        title_text = title_font.render("Space Battle", 1, WHITE)
        play_text = menu_font.render("Press P to Play", 1, WHITE)
        quit_text = menu_font.render("Press Q to Quit", 1, WHITE)

        WIN.blit(SPACE, (0, 0))
        WIN.blit(title_text, (WIDTH / 2 - title_text.get_width() / 2, HEIGHT / 4))
        WIN.blit(play_text, (WIDTH / 2 - play_text.get_width() / 2, HEIGHT / 2))
        WIN.blit(quit_text, (WIDTH / 2 - quit_text.get_width() / 2, HEIGHT / 2 + 50))

        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        menu_running = True

        while menu_running:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        menu_running = False

        game_running = True
        while game_running:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == self.yellow.controls['shoot']:
                        self.yellow.shoot(1)
                    if event.key == self.red.controls['shoot']:
                        self.red.shoot(-1)

                if event.type == RED_HIT:
                    self.red.health -= 1
                    BULLET_HIT_SOUND.play()
                if event.type == YELLOW_HIT:
                    self.yellow.health -= 1
                    BULLET_HIT_SOUND.play()

            winner_text = ""
            if self.red.health <= 0:
                winner_text = "Yellow Wins!"
            elif self.yellow.health <= 0:
                winner_text = "Red Wins!"

            if winner_text:
                self.draw_winner(winner_text)
                pygame.time.delay(2000)
                main()
                return

            keys_pressed = pygame.key.get_pressed()
            self.yellow.move(keys_pressed)
            self.red.move(keys_pressed)

            self.handle_bullets()
            self.draw_window()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
