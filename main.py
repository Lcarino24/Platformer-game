import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (21, 207, 14)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)

# Fonts
smallfont = pygame.font.SysFont('Arial', 25)
medfont = pygame.font.SysFont('Arial', 40)
largefont = pygame.font.SysFont('Arial', 60)
clock = pygame.time.Clock()

# Player Setup
player_width = 50
player_height = 50
player_x = 100
player_y = HEIGHT - player_height - 100
player_velocity = 5
player_jump_velocity = -12
gravity = 0.8
player_velocity_y = 0
is_jumping = False
health = 100
score = 0

# Load Images and Sounds
player_run = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/LebronRaymoneJames.png")
player_jump = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/LebronRaymoneJames.png")
coin_image = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/coin.png")
boss_image = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/Michael Jeffrey Jordan.png")
power_up_image = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/crown.png")
bg_music = "/Users/lucascarino/PycharmProjects/More list/Platformer game/background_music.mp3"
jump_sound = pygame.mixer.Sound("/Users/lucascarino/PycharmProjects/More list/Platformer game/jump-up-245782.mp3")
coin_sound = pygame.mixer.Sound("/Users/lucascarino/PycharmProjects/More list/Platformer game/coin-257878.mp3")
hit_sound = pygame.mixer.Sound("/Users/lucascarino/PycharmProjects/More list/Platformer game/hit.mp3")


# Background Music
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)

# Power-Ups
POWER_UPS = ["speed_boost", "invincibility", "health_restore"]

# Parallax Variables
bg_x = 0
bg_scroll_speed = 2

# Levels
current_level = 1
level_data = {
    1: {"bg": "/Users/lucascarino/PycharmProjects/More list/Platformer game/background.jpeg", "enemy_count": 5, "boss": False},
    2: {"bg": "/Users/lucascarino/PycharmProjects/More list/Platformer game/background.jpeg", "enemy_count": 7, "boss": False},
    3: {"bg": "/Users/lucascarino/PycharmProjects/More list/Platformer game/background.jpeg", "enemy_count": 10, "boss": True},
}

# Classes
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(coin_image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type):
        super().__init__()
        self.image = pygame.transform.scale(power_up_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = power_type

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(boss_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.speed = 3

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.speed *= -1

# Game Logic Functions
def draw_health_bar():
    pygame.draw.rect(window, RED, (20, 20, 200, 20))
    pygame.draw.rect(window, GREEN, (20, 20, 2 * health, 20))

def draw_score():
    score_text = smallfont.render(f"Score: {score}", True, BLACK)
    window.blit(score_text, (WIDTH - 150, 20))

def draw_player():
    if is_jumping:
        window.blit(player_jump, (player_x, player_y))
    else:
        window.blit(player_run, (player_x, player_y))

def draw_background():
    global bg_x
    background_img = pygame.image.load(level_data[current_level]["bg"])
    background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
    window.fill(WHITE)
    window.blit(background_img, (bg_x, 0))
    window.blit(background_img, (bg_x + WIDTH, 0))
    bg_x -= bg_scroll_speed
    if bg_x <= -WIDTH:
        bg_x = 0

def handle_movement():
    global player_x, player_y, player_velocity_y, is_jumping, score
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT]:
        player_x += player_velocity

    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = player_jump_velocity
        is_jumping = True
        jump_sound.play()

    player_velocity_y += gravity
    player_y += player_velocity_y

    if player_y >= HEIGHT - player_height - 100:
        player_y = HEIGHT - player_height - 100
        player_velocity_y = 0
        is_jumping = False

def main_menu():
    while True:
        window.fill(WHITE)
        title_text = largefont.render("Platformer Game", True, BLUE)
        window.blit(title_text, (WIDTH // 3, HEIGHT // 4))

        start_text = medfont.render("Press Enter to Start", True, BLACK)
        window.blit(start_text, (WIDTH // 3, HEIGHT // 2))

        exit_text = medfont.render("Press Esc to Exit", True, BLACK)
        window.blit(exit_text, (WIDTH // 3, HEIGHT // 1.5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

def level_select():
    global current_level
    while True:
        window.fill(WHITE)
        level_text = largefont.render("Select Level", True, BLUE)
        window.blit(level_text, (WIDTH // 3, HEIGHT // 4))

        for i in range(1, 4):
            level_button = medfont.render(f"Level {i}", True, BLACK)
            window.blit(level_button, (WIDTH // 3, HEIGHT // 3 + (i - 1) * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    current_level = 1
                    return
                if event.key == pygame.K_2:
                    current_level = 2
                    return
                if event.key == pygame.K_3:
                    current_level = 3
                    return

def game_loop():
    global health, score, is_jumping, current_level

    coins = [Coin(random.randint(100, 700), random.randint(100, 500)) for _ in range(level_data[current_level]["enemy_count"])]
    power_ups = [PowerUp(random.randint(100, 700), random.randint(100, 500), random.choice(POWER_UPS)) for _ in range(3)]
    boss = BossEnemy(WIDTH - 200, HEIGHT - 150, 150, 150) if level_data[current_level]["boss"] else None

    while True:
        draw_background()
        draw_player()
        draw_health_bar()
        draw_score()

        handle_movement()

        for coin in coins:
            window.blit(coin.image, coin.rect)

        for power_up in power_ups:
            window.blit(power_up.image, power_up.rect)

        if boss:
            boss.update()
            window.blit(boss.image, boss.rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)

def main():
    while True:
        main_menu()
        level_select()
        game_loop()

if __name__ == "__main__":
    main()
