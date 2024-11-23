import pygame #imports pygame module for specific functions that allow smooth game operation
import sys #sys module provides access to functions and variables that are used, maintained, or interact with the interpreter
import random #module that helps generate random numbers

# Initialize pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 600 #dual assignemnt of dimensions for the game
window = pygame.display.set_mode((WIDTH, HEIGHT)) #assigns display window to window variable
pygame.display.set_caption('Platformer Game')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (21, 207, 14)
BLUE = (0, 0, 255)
YELLOW = (255, 215, 0)

# Fonts
smallfont = pygame.font.SysFont('gillsansultra', 25)
medfont = pygame.font.SysFont('gillsansultra', 40)
largefont = pygame.font.SysFont('gillsansultra', 60)
clock = pygame.time.Clock()

# Player Setup
player_width = 50
player_height = 50
player_x = 100 #initial x position of character
player_y = HEIGHT - player_height - 100 #initial y position of character
player_velocity = 5
player_jump_velocity = -12 #negative value because y-axis points downwards
gravity = 0.8 #force pulling down on player
player_velocity_y = 0 #initial variable that indicates player y velocity when not jumping
is_jumping = False #inital boolean value assigned to whether player is jumping or not
health = 100 #initializion of health
score = 0 #initializtion of score


def scale_image(image, max_width, max_height): #This function scales an image such that it fits in the parameters given in the function while preserving the aspect ratio
    original_width, original_height = image.get_size()
    aspect_ratio = original_width / original_height

    # Determine new width and height while maintaining aspect ratio
    if max_width / max_height > aspect_ratio: #if the image is smaller width-wise, it is resized according to the max height while preserving the aspect ratio
        new_width = int(max_height * aspect_ratio)
        new_height = max_height
    else: # if else, the image is greater width wise and thus is adjusted according to the max width while preserving the aspect ratio.
        new_width = max_width
        new_height = int(max_width / aspect_ratio)

    return pygame.transform.scale(image, (new_width, new_height)) # returns the resized image as a pygame surface object


# Load Images and Sounds. Uses the previously defined function to resize images for specific instances and assign them to variables
player_run = scale_image(
    pygame.image.load("LebronRaymoneJames.png"),
    player_width, player_height)
player_jump = scale_image(
    pygame.image.load("LebronRaymoneJames.png"),
    player_width, player_height)
coin_image = scale_image(pygame.image.load("coin.png"), 30,
                         30)
boss_image = scale_image(
    pygame.image.load("Michael Jeffrey Jordan.png"), 150,
    150)
power_up_image = scale_image(
    pygame.image.load("crown.png"), 40, 40)
bg_music = "background_music.mp3"
jump_sound = pygame.mixer.Sound("jump-up-245782.mp3")
coin_sound = pygame.mixer.Sound("coin-257878.mp3")
hit_sound = pygame.mixer.Sound("hit.mp3")

# Background Music
pygame.mixer.music.load(bg_music)
pygame.mixer.music.play(-1) #plays music on repeat

# Power-Ups
POWER_UPS = ["speed_boost", "invincibility", "health_restore"] #list of indexable power ups

# Parallax Variables
bg_x = 0 #initial position of the background image
bg_scroll_speed = 2 # variable assigned to the scroll speed of the background

# Levels
current_level = 1
level_data = {
    1: {"bg": "background.jpeg", "enemy_count": 3,
        "boss": False},
    2: {"bg": "background.jpeg", "enemy_count": 4,
        "boss": False},
    3: {"bg": "background.jpeg", "enemy_count": 5,
        "boss": True},
} # indexable dictionary in a dictionary that contains level information for each specfied level

# Classes
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y): # initializes the x and y positions of the coins in levels
        super().__init__()
        self.image = pygame.transform.scale(coin_image, (30, 30)) #loads the coins image and resizes it
        self.rect = self.image.get_rect(topleft=(x, y)) # defines rectangular body for positioning and collision detection as well as places the top left corner of the image at (x,y)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, power_type): # initializes the x and y positions of the power up as well as includes an additional argument for power-up type
        super().__init__()
        self.image = pygame.transform.scale(power_up_image, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.type = power_type  # Power type (e.g., speed_boost, invincibility, health_restore)


class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.transform.scale(boss_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = 100 # initializes the bosses health
        self.speed = 3 # initializes the bosses speed

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed): # initializes the position, dimensions, and speed of the enemy
        super().__init__()
        self.image = pygame.image.load("Steph Curry.png")
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.gravity = 0.8
        self.vertical_velocity = 0
        self.is_jumping = False
        self.jump_timer = random.randint(100, 200)  # Timer for random jumps

    def update(self):
        # Horizontal movement
        self.rect.x += self.speed
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed *= -1  # Reverse direction

        # Random jumping logic
        if current_level in [2, 3]:  # Enable jumping in levels 2 and 3
            self.jump_timer -= 1
            if self.jump_timer <= 0 and not self.is_jumping:
                self.vertical_velocity = -10  # Set jump velocity
                self.is_jumping = True
                self.jump_timer = random.randint(100, 200)  # Reset timer

            # Apply gravity
            self.vertical_velocity += self.gravity
            self.rect.y += self.vertical_velocity

            # Check if the enemy lands on the ground
            if self.rect.bottom >= HEIGHT - 100:
                self.rect.bottom = HEIGHT - 100
                self.vertical_velocity = 0
                self.is_jumping = False


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

def draw_background_main():
    background_img1 = pygame.image.load("bball_bg.jpg")
    background_img1 = pygame.transform.scale(background_img1, (WIDTH, HEIGHT))
    window.blit(background_img1, (0,0))


def handle_movement():
    global player_x, player_y, player_velocity_y, is_jumping, score

    keys = pygame.key.get_pressed()

    # Horizontal movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_x -= player_velocity
        if player_x < 0:  # Prevent the player from moving off the left side of the screen
            player_x = 0

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player_x += player_velocity
        if player_x > WIDTH - player_width:  # Prevent the player from moving off the right side of the screen
            player_x = WIDTH - player_width

    # Vertical movement (jumping and gravity)
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and not is_jumping:
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
        #window.fill(WHITE)
        draw_background_main()
        #background, bg_image = get_background("bball_bg.jpg")
        title_text = largefont.render("Super Lebron", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//4))
        window.blit(title_text, title_rect)

        start_text = medfont.render("Press Enter to Start", True, WHITE)
        start_rect = start_text.get_rect(center=(WIDTH// 2, HEIGHT// 2 ))
        window.blit(start_text, start_rect)

        pygame.draw.circle(window, (0, 132, 255), (30, 30), 30)
        pygame.draw.polygon(window, WHITE, ((30, 5), (30, 55), (5, 30)))
        pygame.draw.rect(window, WHITE, (30, 18, 25, 25))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            mousepos = pygame.mouse.get_pos()
            mousex = int(mousepos[0])
            mousey = int(mousepos[1])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    level_select()
                    return
            if 0 <= mousex <= 60 and 0 <= mousey <= 60 and event.type == pygame.MOUSEBUTTONDOWN:
                pygame.quit()
                sys.exit()

def game_over(start_x, start_y, start_health, start_score):
    global health, score
    while True:
        window.fill(WHITE)
        game_over_text = largefont.render("Game Over", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        window.blit(game_over_text, game_over_rect)
        #window.blit(game_over_text, (WIDTH // 3.25, HEIGHT // 4))

        score_text = medfont.render(f"Final Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(score_text, score_rect)

        restart_text = smallfont.render("Press Enter to return to Level Select", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 * 3))
        window.blit(restart_text, restart_rect)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    level_select()
                    return

# Global variable for high score
high_scores = {1: None, 2: None, 3: None}  # High scores for levels
import time

def game_loop():
    global health, score, is_jumping, current_level, player_x, player_y, player_velocity_y, high_scores

    # Reset player state for the new level
    health = 100
    score = 0
    is_jumping = False
    player_x, player_y = 100, HEIGHT - player_height - 100  # Reset position
    player_velocity_y = 0

    # Initialize start time
    start_time = pygame.time.get_ticks()

    # Create coins, power-ups, and enemies for the current level
    coins = [Coin(random.randint(100, 700), random.randint(340, 490)) for _ in
             range(level_data[current_level]["enemy_count"])]
    power_ups = [PowerUp(random.randint(100, 700), random.randint(340, 490), random.choice(POWER_UPS)) for _ in
                 range(3)]
    enemies = [Enemy(random.randint(50, WIDTH - 50), HEIGHT - player_height - 100, 50, 50, random.choice([-3, 3])) for _
               in range(level_data[current_level]["enemy_count"])]
    boss = BossEnemy(WIDTH - 200, HEIGHT - 150, 150, 150) if level_data[current_level]["boss"] else None

    # Reset power-up variables
    power_up_message = ""
    active_power_up = None
    power_up_start_time = None
    power_up_duration = 5

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
                coins.remove(coin)
                score += 1
                coin_sound.play()

        # Draw and update power-ups
        for power_up in power_ups:
            window.blit(power_up.image, power_up.rect)

            # Check for collisions with power-ups
            if player_x < power_up.rect.right and player_x + player_width > power_up.rect.left and \
                    player_y < power_up.rect.bottom and player_y + player_height > power_up.rect.top:
                power_up_effect = power_up.type
                power_ups.remove(power_up)

                active_power_up = power_up_effect
                power_up_message = f"You got {active_power_up}!"
                power_up_start_time = time.time()

                if active_power_up == "speed_boost":
                    player_velocity = 20
                elif active_power_up == "invincibility":
                    health = min(health + 50, 100)
                elif active_power_up == "health_restore":
                    health = 100
                coin_sound.play()

        # Check if all coins and power-ups are collected
        if not coins and not power_ups:
            elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert milliseconds to seconds
            update_high_score(elapsed_time)
            won_level(player_x, player_y, health, score, elapsed_time)
            return

        # Handle enemies and collisions
        for enemy in enemies:
            enemy.update()
            window.blit(enemy.image, enemy.rect)

            if player_x < enemy.rect.right and player_x + player_width > enemy.rect.left and \
                    player_y < enemy.rect.bottom and player_y + player_height > enemy.rect.top:
                if active_power_up != "invincibility":
                    health -= 1.5
                    hit_sound.play()

        if boss:
            boss.update()
            window.blit(boss.image, boss.rect)

        # Handle power-up timer expiration
        if active_power_up:
            power_up_text = smallfont.render(power_up_message, True, YELLOW)
            power_up_rect = power_up_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
            window.blit(power_up_text, power_up_rect)

        if power_up_start_time and time.time() - power_up_start_time > power_up_duration:
            if active_power_up == "speed_boost":
                player_velocity = 5
            active_power_up = None
            power_up_message = ""

        if health <= 0:
            game_over(100, HEIGHT - player_height - 100, 100, 0)
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
        clock.tick(60)


import json

# File to store high scores
HIGH_SCORE_FILE = "high_scores.json"


def load_high_scores():
    global high_scores
    try:
        with open(HIGH_SCORE_FILE, 'r') as file:
            high_scores = json.load(file)
            # Ensure all levels have keys in the high_scores dictionary
            high_scores = {int(k): v for k, v in high_scores.items()}  # Convert keys to integers
    except (FileNotFoundError, json.JSONDecodeError):
        # Initialize default high scores if file is missing or corrupted
        high_scores = {1: None, 2: None, 3: None}

    # Ensure all levels are present
    for level in range(1, 4):
        if level not in high_scores:
            high_scores[level] = None


def save_high_scores():
    with open(HIGH_SCORE_FILE, 'w') as file:
        json.dump(high_scores, file)


def update_high_score(elapsed_time):
    global high_scores, current_level

    if high_scores[current_level] is None or elapsed_time < high_scores[current_level]:
        high_scores[current_level] = elapsed_time
        save_high_scores()  # Save the updated high scores to the file

def won_level(start_x, start_y, start_health, start_score, elapsed_time):
    global health, score
    while True:
        window.fill(WHITE)
        win_text = largefont.render("You Won!", True, GREEN)
        win_rect = win_text.get_rect(center=(WIDTH // 2, HEIGHT// 4))
        window.blit(win_text, win_rect)

        score_text = medfont.render(f"Final Score: {score}", True, BLACK)
        score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        window.blit(score_text, score_rect)

        time_text = medfont.render(f"Time: {elapsed_time:.2f}s", True, BLACK)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
        window.blit(time_text, time_rect)

        restart_text = smallfont.render("Press Enter to return to Level Select", True, BLACK)
        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.2))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    level_select()
                    return  # Exit the function to return to the caller
def level_select():
    global current_level, health, score, player_x, player_y, player_velocity_y
    while True:
        window.fill(WHITE)
        level_text = largefont.render("Select Level", True, BLUE)
        window.blit(level_text, (WIDTH // 3, HEIGHT // 4))
        pygame.draw.circle(window, (0, 132, 255), (30, 30), 30)
        pygame.draw.polygon(window, WHITE, ((30, 5), (30, 55), (5, 30)))
        pygame.draw.rect(window, WHITE, (30, 18, 25, 25))
        for i in range(1, 4):
            level_button = medfont.render(f"Level {i}", True, BLACK)
            high_score_text = smallfont.render(
                f"Best Time: {high_scores[i]:.2f}s" if high_scores[i] else "No Record",
                True, GREEN
            )
            window.blit(level_button, (WIDTH // 3, HEIGHT // 3 + (i - 1) * 50))
            window.blit(high_score_text, (WIDTH // 3 + 150, HEIGHT // 3 + (i - 1) * 50))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            mousepos = pygame.mouse.get_pos()
            mousex = int(mousepos[0])
            mousey = int(mousepos[1])

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    health = 100
                    score = 0
                    player_x = 100
                    player_y = HEIGHT - player_height - 100
                    player_velocity_y = 0
                    current_level = 1
                    game_loop()
                    return
                elif event.key == pygame.K_2:
                    health = 100
                    score = 0
                    player_x = 100
                    player_y = HEIGHT - player_height - 100
                    player_velocity_y = 0
                    current_level = 2
                    game_loop()
                    return
                elif event.key == pygame.K_3:
                    health = 100
                    score = 0
                    player_x = 100
                    player_y = HEIGHT - player_height - 100
                    player_velocity_y = 0
                    current_level = 3
                    game_loop()
                    return
            if 0 <= mousex <= 60 and 0 <= mousey <= 60 and event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()
                return




def main():
    load_high_scores()  # Load saved high scores
    while True:
        main_menu()
        level_select()
        game_loop()


if __name__ == "__main__":
    main()
