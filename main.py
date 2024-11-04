import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Screen Setup
WIDTH, HEIGHT = 800, 600
Window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Platformer Game')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
green = (21, 207, 14)
red = (255, 0, 0)
blue = (0, 14, 204)
brown = (216, 180, 119)
dark_red = (155, 45, 36)

# Fonts
tinyfont = pygame.font.SysFont('calibri', 18)
smallfont = pygame.font.SysFont('timesnewroman', 25)
medfont = pygame.font.SysFont('timesnewroman', 40)
largefont = pygame.font.SysFont('timesnewroman', 75)
font = pygame.font.SysFont(None, 25)
clock = pygame.time.Clock()

# Player Setup
player_width = 50
player_height = 50
player_color = green
player_x = 100
player_y = HEIGHT - player_height - 100
player_velocity = 5
player_jump_velocity = -12
is_jumping = False
jump_height = 10

# Platform Setup
platform_color = blue
platforms = [(0, HEIGHT - 50, WIDTH, 50)]  # Ground platform

# Game Variables
gravity = 0.8
player_velocity_y = 0
is_game_over = False
level = 1  # Start with level 1


# Load images
def load_image(image_path):
    try:
        image = pygame.image.load("/Users/lucascarino/PycharmProjects/More list/Platformer game/mainmenu.jpg")
        return pygame.transform.scale(image, (800, 600))  # Rescale image
    except pygame.error as e:
        print(f"Error loading image: {e}")
        return None


main_menu_img = load_image('/Users/lucascarino/PycharmProjects/More list/Platformer game/mainmenu.jpg')


# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.width:
            self.rect.x = WIDTH


# Timer Setup
start_time = time.time()

# Leaderboard Setup
highscores = {"Level 1": 0, "Level 2": 0, "Level 3": 0}


# Text and Button functions
def text_objects(text, colour, size='small'):
    if size == 'tiny':
        textSurface = tinyfont.render(text, True, colour)
    if size == 'small':
        textSurface = smallfont.render(text, True, colour)
    if size == 'medium':
        textSurface = medfont.render(text, True, colour)
    if size == 'large':
        textSurface = largefont.render(text, True, colour)

    return textSurface, textSurface.get_rect()


def text_to_button(msg, colour, button_x, button_y, button_width, button_height, size='small'):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = ((button_x + (button_width / 2)), button_y + (button_height / 2))
    Window.blit(textSurf, textRect)


def message_to_screen(msg, colour, cordy=0, size='small'):
    textSurf, textRect = text_objects(msg, colour, size)
    textRect.center = (int(800 / 2), int(600 / 2) + cordy)
    Window.blit(textSurf, textRect)


def draw_player(x, y):
    pygame.draw.rect(Window, player_color, (x, y, player_width, player_height))


def draw_platforms():
    for plat in platforms:
        pygame.draw.rect(Window, platform_color, plat)


def handle_player_movement():
    global player_x, player_y, player_velocity_y, is_jumping
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        player_x -= player_velocity
    if keys[pygame.K_RIGHT]:
        player_x += player_velocity
    if keys[pygame.K_UP] and not is_jumping:
        is_jumping = True
        player_velocity_y = player_jump_velocity

    # Apply gravity
    player_y += player_velocity_y
    if player_y < HEIGHT - player_height - 50:
        player_velocity_y += gravity  # Simulate gravity
    else:
        player_y = HEIGHT - player_height - 50  # Reset player to ground level
        if is_jumping:
            is_jumping = False

    # Prevent player from going off the left side of the screen
    if player_x < 0:
        player_x = 0

    # Prevent player from going off the right side of the screen
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width


def check_collisions():
    global player_x, player_y
    for plat in platforms:
        plat_x, plat_y, plat_w, plat_h = plat
        if player_y + player_height > plat_y and player_y + player_height < plat_y + 10:
            if plat_x < player_x + player_width and plat_x + plat_w > player_x:
                return True
    return False


def check_enemy_collisions():
    global player_x, player_y
    for enemy in enemies:
        if enemy.rect.x < player_x + player_width and enemy.rect.x + enemy.width > player_x:
            if enemy.rect.y < player_y + player_height and enemy.rect.y + enemy.height > player_y:
                return True
    return False


def level_1():
    global platforms, enemies
    platforms = [(0, HEIGHT - 50, WIDTH, 50)]  # Ground level platform only
    enemies = [Enemy(600, HEIGHT - 100, 50, 50, red)]  # Add enemies to the level
    while True:
        Window.fill(white)
        message_to_screen('Level 1 - Easy', red, -200, 'large')
        message_to_screen('Press LEFT/RIGHT to move and UP to jump', black, 50, 'small')
        draw_player(player_x, player_y)
        draw_platforms()

        for enemy in enemies:
            enemy.update()
            Window.blit(enemy.image, enemy.rect)

        handle_player_movement()
        if check_collisions():
            player_velocity_y = 0  # Stop falling when player lands on a platform
        if check_enemy_collisions():
            message_to_screen('Game Over!', red, 0, 'large')
            pygame.display.update()
            pygame.time.wait(2000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)


def level_2():
    global platforms, enemies
    platforms = [(0, HEIGHT - 50, WIDTH, 50), (200, HEIGHT - 150, 200, 10)]  # Added a platform
    enemies = [Enemy(600, HEIGHT - 100, 50, 50, red), Enemy(500, HEIGHT - 200, 50, 50, red)]  # Add more enemies
    while True:
        Window.fill(white)
        message_to_screen('Level 2 - Medium Difficulty', red, -200, 'large')
        message_to_screen('Watch out for new platforms and enemies!', black, 50, 'small')
        draw_player(player_x, player_y)
        draw_platforms()

        for enemy in enemies:
            enemy.update()
            Window.blit(enemy.image, enemy.rect)

        handle_player_movement()
        if check_collisions():
            player_velocity_y = 0  # Stop falling when player lands on a platform
        if check_enemy_collisions():
            message_to_screen('Game Over!', red, 0, 'large')
            pygame.display.update()
            pygame.time.wait(2000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)


def level_3():
    global platforms, enemies
    platforms = [(0, HEIGHT - 50, WIDTH, 50), (200, HEIGHT - 150, 200, 10),
                 (500, HEIGHT - 250, 200, 10)]  # More complex platforms
    enemies = [Enemy(600, HEIGHT - 100, 50, 50, red), Enemy(400, HEIGHT - 200, 50, 50, red),
               Enemy(700, HEIGHT - 300, 50, 50, red)]  # Add even more enemies
    while True:
        Window.fill(white)
        message_to_screen('Level 3 - Hard', red, -200, 'large')
        message_to_screen('Fast enemies and hard jumps!', black, 50, 'small')
        draw_player(player_x, player_y)
        draw_platforms()

        for enemy in enemies:
            enemy.update()
            Window.blit(enemy.image, enemy.rect)

        handle_player_movement()
        if check_collisions():
            player_velocity_y = 0  # Stop falling when player lands on a platform
        if check_enemy_collisions():
            message_to_screen('Game Over!', red, 0, 'large')
            pygame.display.update()
            pygame.time.wait(2000)
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()
        clock.tick(60)


def intro():
    while True:
        Window.fill(white)
        Window.blit(main_menu_img, (0, 0))
        message_to_screen('Welcome to the Platformer Game!', red, -200, 'large')
        message_to_screen('Select a level to play:', black, 100, 'small')

        pygame.draw.rect(Window, green, (125, 450, 150, 50))
        message_to_screen('Level 1', black, 450, 'small')

        pygame.draw.rect(Window, blue, (325, 450, 150, 50))
        message_to_screen('Level 2', black, 450, 'small')

        pygame.draw.rect(Window, red, (525, 450, 150, 50))
        message_to_screen('Level 3', black, 450, 'small')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            mouse_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 125 <= mouse_pos[0] <= 275 and 450 <= mouse_pos[1] <= 500:
                    level_1()
                elif 325 <= mouse_pos[0] <= 475 and 450 <= mouse_pos[1] <= 500:
                    level_2()
                elif 525 <= mouse_pos[0] <= 675 and 450 <= mouse_pos[1] <= 500:
                    level_3()

        pygame.display.update()
        clock.tick(15)


# Start the game
intro()
