import pygame
import sys
import time
import random

# Initialize pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 600
Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer Game - Power-Ups & Enhanced Boss Fight')

# Colors
white = (255, 255, 255)
red = (255, 0, 0)
green = (21, 207, 14)
black = (0, 0, 0)
gold = (255, 215, 0)
blue = (0, 0, 255)
purple = (128, 0, 128)

# Fonts
smallfont = pygame.font.SysFont('timesnewroman', 25)
medfont = pygame.font.SysFont('timesnewroman', 40)
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
invincible = False
speed_boost = False
power_up_timer = 0

# Load Images and Sounds
player_run = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/LebronRaymoneJames.png")
player_jump = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/LebronRaymoneJames.png")
coin_image = pygame.image.load("assets/coin.png")
boss_image = pygame.image.load("assets/boss.png")
power_up_image = pygame.image.load("assets/power_up.png")
jump_sound = pygame.mixer.Sound("/Users/lucascarino/PycharmProjects/More list/Platformer game/jump-up-245782.mp3")
hit_sound = pygame.mixer.Sound("assets/hit.wav")
coin_sound = pygame.mixer.Sound("assets/coin.wav")
power_up_sound = pygame.mixer.Sound("assets/power_up.wav")
bg_music = "/Users/lucascarino/PycharmProjects/More list/Platformer game/background_music.mp3"

# Background Music
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1)

# Power-Up Types
POWER_UPS = ["speed_boost", "invincibility", "health_restore"]

# Parallax Variables
bg_x = 0
bg_scroll_speed = 2

# Coin Class
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(coin_image, (30, 30))
        self.rect = self.image.get_rect(topleft=(x, y))

# PowerUp Class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type):
        super().__init__()
        self.image = pygame.transform.scale(power_up_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = power_type

# BossEnemy Class with Attack Patterns
class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(boss_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.speed = 3
        self.attack_timer = 0
        self.is_charging = False

    def update(self):
        if self.is_charging:
            self.rect.x -= self.speed * 2
        else:
            self.rect.x -= self.speed

        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.speed *= -1

        # Randomize attack pattern
        self.attack_timer += 1
        if self.attack_timer > 200:
            self.attack_pattern()
            self.attack_timer = 0

    def attack_pattern(self):
        # Choose a random attack
        attack_choice = random.choice(["charge", "shoot"])
        if attack_choice == "charge":
            self.is_charging = True
        else:
            self.is_charging = False

# Health Bar
def draw_health_bar():
    pygame.draw.rect(Window, red, (20, 20, 200, 20))
    pygame.draw.rect(Window, green, (20, 20, 2 * health, 20))

# Score Display
def draw_score():
    score_text = smallfont.render(f"Score: {score}", True, black)
    Window.blit(score_text, (WIDTH - 150, 20))

# Draw Player with Animation
def draw_player(frame):
    if invincible:
        player_color = purple
    elif speed_boost:
        player_color = blue
    else:
        player_color = green

    if is_jumping:
        Window.blit(player_jump, (player_x, player_y))
    else:
        Window.blit(player_run[frame // 5], (player_x, player_y))

# Parallax Scrolling
def draw_background():
    global bg_x
    Window.fill(white)
    Window.blit(background_img, (bg_x, 0))
    Window.blit(background_img, (bg_x + WIDTH, 0))
    bg_x -= bg_scroll_speed
    if bg_x <= -WIDTH:
        bg_x = 0

# Power-Up Effects
def activate_power_up(power_type):
    global invincible, speed_boost, health, power_up_timer
    if power_type == "speed_boost":
        speed_boost = True
        power_up_timer = 300
        power_up_sound.play()
    elif power_type == "invincibility":
        invincible = True
        power_up_timer = 300
        power_up_sound.play()
    elif power_type == "health_restore":
        health = min(health + 30, 100)
        power_up_sound.play()

# Main Game Loop
def game_loop():
    frame = 0
    global health, score, invincible, speed_boost, power_up_timer
    coins = [Coin(random.randint(100, 700), random.randint(100, 500)) for _ in range(10)]
    power_ups = [PowerUp(random.randint(100, 700), random.randint(100, 500), random.choice(POWER_UPS)) for _ in range(5)]
    boss = BossEnemy(WIDTH - 200, HEIGHT - 150, 150, 150)

    while True:
        draw_background()
        draw_player(frame)
        draw_health_bar()
        draw_score()

        # Update and draw coins
        for coin in coins:
            Window.blit(coin.image, coin.rect)

        # Update and draw power-ups
        for power_up in power_ups:
            Window.blit(power_up.image, power_up.rect)
            if power_up.rect.colliderect((player_x, player_y, player_width, player_height)):
                activate_power_up(power_up.type)
                power_ups.remove(power_up)

        # Boss fight logic
        boss.update()
        Window.blit(boss.image, boss.rect)

        if invincible:
            boss.is_charging = False

        if power_up_timer > 0:
            power_up_timer -= 1
        else:
            invincible = False
            speed_boost = False

        handle_movement()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        frame += 1
        if frame >= 20:
            frame = 0

        pygame.display.update()
        clock.tick(60)

# Start the Game
game_loop()
