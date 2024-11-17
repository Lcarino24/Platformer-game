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
def scale_image(image, max_width, max_height):
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height

    # Determine new width and height while maintaining aspect ratio
    if max_width / max_height > aspect_ratio:
        new_width = int(max_height * aspect_ratio)
        new_height = max_height
    else:
        new_width = max_width
        new_height = int(max_width / aspect_ratio)

    return pygame.transform.scale(image, (new_width, new_height))

# Load Images and Sounds
player_run = scale_image(pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/LebronRaymoneJames.png"), player_width, player_height)
player_jump = scale_image(pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/LebronRaymoneJames.png"), player_width, player_height)
coin_image = scale_image(pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/coin.png"), 30, 30)
boss_image = scale_image(pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/Michael Jeffrey Jordan.png"), 150, 150)
power_up_image = scale_image(pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/crown.png"), 40, 40)
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
        self.type = power_type  # Power type (e.g., speed_boost, invincibility, health_restore)


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(boss_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100
        self.speed = 3
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/Steph Curry.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x += self.speed
        # Reverse direction when hitting the screen boundaries
        if self.rect.right >= WIDTH or self.rect.left <= 0:
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
    window.blit(background_img, (0, 0))
    bg_x -= bg_scroll_speed
    if bg_x <= -WIDTH:
        bg_x = 0


def handle_movement():
    global player_x, player_y, player_velocity_y, is_jumping, score

    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_LEFT]:
        player_x -= player_velocity
        if player_x < 0:  # Prevent the player from moving off the left side of the screen
            player_x = 0

    if keys[pygame.K_RIGHT]:
        player_x += player_velocity
        if player_x > WIDTH - player_width:  # Prevent the player from moving off the right side of the screen
            player_x = WIDTH - player_width

    # Vertical movement (jumping and gravity)
    if keys[pygame.K_SPACE] and not is_jumping:
        player_velocity_y = player_jump_velocity
        is_jumping = True
        jump_sound.play()

    # Apply gravity
    player_velocity_y += gravity
    player_y += player_velocity_y

    # Prevent the player from falling through the ground
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

import time  # Import the time module for handling timing

def game_loop():
    global health, score, is_jumping, current_level, player_x, player_y, player_velocity_y

    # Store initial player position and other variables to reset later
    initial_player_x = 100
    initial_player_y = HEIGHT - player_height - 100
    initial_health = 100
    initial_score = 0

    # Create coins, power-ups, and enemies
    coins = [Coin(random.randint(100, 700), random.randint(100, 500)) for _ in range(level_data[current_level]["enemy_count"])]
    power_ups = [PowerUp(random.randint(100, 700), random.randint(100, 500), random.choice(POWER_UPS)) for _ in range(3)]
    enemies = [Enemy(random.randint(50, WIDTH - 50), HEIGHT - player_height - 100, 50, 50, random.choice([-3, 3])) for _ in range(level_data[current_level]["enemy_count"])]
    boss = BossEnemy(WIDTH - 200, HEIGHT - 150, 150, 150) if level_data[current_level]["boss"] else None

    # Power-up effect display text
    power_up_message = ""
    active_power_up = None
    power_up_start_time = None  # Store the start time of the power-up effect
    power_up_duration = 5  # Duration of the power-up effect (in seconds)

    while True:
        draw_background()
        draw_player()
        draw_health_bar()
        draw_score()

        handle_movement()

        # Draw and update coins
        for coin in coins:
            window.blit(coin.image, coin.rect)

        # Check for collisions with coins
        for coin in coins[:]:
            if player_x < coin.rect.right and player_x + player_width > coin.rect.left and \
               player_y < coin.rect.bottom and player_y + player_height > coin.rect.top:
                # Coin collision detected
                coins.remove(coin)  # Remove the coin from the list
                score += 1  # Increase the score
                coin_sound.play()  # Play coin sound

        # Draw and update power-ups
        for power_up in power_ups:
            window.blit(power_up.image, power_up.rect)

            # Check for collisions with power-ups
            if player_x < power_up.rect.right and player_x + player_width > power_up.rect.left and \
               player_y < power_up.rect.bottom and player_y + player_height > power_up.rect.top:
                # Power-up collision detected
                power_up_effect = power_up.type  # Get the type of power-up
                power_ups.remove(power_up)  # Remove the power-up from the list

                # Assign the random power-up effect
                active_power_up = power_up_effect
                power_up_message = f"You got {active_power_up}!"
                power_up_start_time = time.time()  # Capture the start time of the power-up

                # Apply the effect
                if active_power_up == "speed_boost":
                    player_velocity = 10  # Increase speed
                elif active_power_up == "invincibility":
                    health = min(health + 50, 100)  # Restore health (as an example)
                elif active_power_up == "health_restore":
                    health = 100  # Restore full health
                coin_sound.play()  # Play the power-up sound

        # Draw and update enemies
        for enemy in enemies:
            enemy.update()
            window.blit(enemy.image, enemy.rect)

            # Check collision with the player
            if player_x < enemy.rect.right and player_x + player_width > enemy.rect.left and \
               player_y < enemy.rect.bottom and player_y + player_height > enemy.rect.top:
                # If the player has the invincibility power-up, they don't take damage
                if active_power_up != "invincibility":
                    health -= 1
                    hit_sound.play()

        # Draw and update boss if present
        if boss:
            boss.update()
            window.blit(boss.image, boss.rect)

        # Display the power-up message
        if active_power_up:
            power_up_text = smallfont.render(power_up_message, True, YELLOW)
            window.blit(power_up_text, (WIDTH // 3, HEIGHT // 3))  # Display in the center of the screen

        # Check if the power-up duration has expired
        if power_up_start_time and time.time() - power_up_start_time > power_up_duration:
            # Reset the power-up effect after the duration
            if active_power_up == "speed_boost":
                player_velocity = 5  # Revert to normal speed
            elif active_power_up == "invincibility":
                # Invincibility effect ends (we can leave this as is for now, or apply additional logic)
                pass
            elif active_power_up == "health_restore":
                # No need to reset health as it was fully restored
                pass

            # Reset the power-up
            active_power_up = None
            power_up_message = ""  # Clear the message

        # Check if the player's health reaches zero
        if health <= 0:
            game_over(initial_player_x, initial_player_y, initial_health, initial_score)
            return  # Stop the game loop and return to the main menu or exit

        # Check for game exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)
def game_over(start_x, start_y, start_health, start_score):
    global player_x, player_y, health, score
    player_x, player_y = start_x, start_y  # Reset player position
    health = start_health  # Reset health
    while True:
        window.fill(WHITE)
        game_over_text = largefont.render("Game Over", True, RED)
        window.blit(game_over_text, (WIDTH // 3, HEIGHT // 4))
        score_text = medfont.render(f"Final Score: {score}", True, BLACK)
        window.blit(score_text, (WIDTH // 3, HEIGHT // 2))
        restart_text = smallfont.render("Press Enter--> Start screen", True, BLACK)
        window.blit(restart_text, (WIDTH // 3, HEIGHT // 1.5))


        pygame.display.update()

        # Check for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Restart the game
                    health = 100  # Reset health
                    score = 0  # Reset score
                    main()  # Call main() to restart the game
                    return


def main():
    while True:
        main_menu()
        level_select()
        game_loop()

if __name__ == "__main__":
    main()

