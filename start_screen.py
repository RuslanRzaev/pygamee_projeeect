import pygame

from pygamee_projeeect.utils import max_attempt
from utils import load_image, get_achievements, terminate, get_number_of_achievements_per_level, get_count_achievement

pygame.init()

SIZE = WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Стартовое окно")

BACKGROUND_IMG = load_image('space_station_800_600.png')
CROSS = pygame.transform.smoothscale(load_image('cross.png'), (30, 30))
CHECK_MARK = pygame.transform.smoothscale(load_image('check_mark.png'), (30, 30))
GITHUB_IMAGE = [load_image('github_ruslan.png'), None, load_image('github_jane.png')]
TG_IMAGE = [load_image('tg_ruslan.png'), load_image('tg_kuzma.png'), load_image('tg_jane.png')]
BLACK = (0, 0, 0)
BUTTON_COLOR = (255, 255, 255)
BUTTON_CLICKED_COLOR = (0, 255, 0)
FPS = 60

# Состояния экрана
SCREEN_MAIN_MENU = "main_menu"
SCREEN_ACHIEVEMENTS = "achievements"
SCREEN_ACHIEVEMENT_DETAIL = "achievement_detail"
SCREEN_ABOUT_AUTHOR = 'about_author'

SELECTED_ATTEMPT = 0

current_screen = SCREEN_MAIN_MENU

font = pygame.font.Font(None, 40)

# событие перехода к игры
lets_go = pygame.event.custom_type()


class Button:
    def __init__(self, x, y, width, height, text, function=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.function = function

    def draw(self, screen):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            pygame.draw.rect(screen, BUTTON_CLICKED_COLOR, self.rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        text = font.render(self.text, True, BLACK)
        screen.blit(text, (self.rect.x + 10, self.rect.y + 10))

    def is_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_x, mouse_y):
                return True
        return False


play_button = Button(300, 200, 200, 50, "Играть")
achievements_button = Button(300, 300, 200, 50, "Достижения", lambda: set_screen(SCREEN_ACHIEVEMENTS))
about_the_authors = Button(300, 400, 200, 50, "Об авторах", lambda: set_screen(SCREEN_ABOUT_AUTHOR))


class Achievement:
    def __init__(self, attempt, name, description, icon_path, date, check, level):
        self.attempt = attempt
        self.name = name
        self.description = description
        self.icon_path = icon_path
        self.image = load_image(icon_path)
        self.date = date
        self.check = check
        self.level = level

    def draw(self, screen, x, y):
        screen.blit(pygame.transform.scale(self.image, (50, 50)), (x, y))
        name = font.render(self.name, True, BUTTON_COLOR)
        screen.blit(name, (x + 60, y))
        if self.check:
            screen.blit(CHECK_MARK, (750, y))
            count_achievement = font.render(
                f'Количество получений: {get_count_achievement(self.level, self.name)}',
                True, BUTTON_COLOR)
            screen.blit(count_achievement, (x + 60, y + 30))
        else:
            screen.blit(CROSS, (750, y))


selected_achievement: Achievement = Achievement | None


def show_main_menu(events):
    play_button.draw(screen)
    achievements_button.draw(screen)
    about_the_authors.draw(screen)
    for event in events:
        if play_button.is_pressed(event):
            pygame.event.post(pygame.event.Event(lets_go))
        if achievements_button.is_pressed(event):
            achievements_button.function()
        if about_the_authors.is_pressed(event):
            about_the_authors.function()

def next_attempt():
    global SELECTED_ATTEMPT
    if SELECTED_ATTEMPT == max_attempt():
        return
    SELECTED_ATTEMPT += 1

def back_attempt():
    global SELECTED_ATTEMPT
    if SELECTED_ATTEMPT == 0:
        return
    SELECTED_ATTEMPT -= 1

def draw_achievements(events):
    global selected_achievement

    achievements = get_achievements(SELECTED_ATTEMPT)
    y_offset = 100
    back_button = Button(10, 10, 100, 40, "Назад", lambda: set_screen(SCREEN_MAIN_MENU))
    button_back_attempt = Button(WIDTH // 2, 50, 120, 40, 'Back', lambda: back_attempt())
    button_back_attempt.draw(screen)
    attempt_level = font.render(f'{SELECTED_ATTEMPT} attempt', True, BUTTON_COLOR)
    screen.blit(attempt_level, (WIDTH // 2 + 130, 50))
    button_next = Button(WIDTH // 2 + 270, 50, 120, 40, 'Next', lambda: next_attempt())
    button_next.draw(screen)
    for achievement_data in achievements:
        achievement = Achievement(*achievement_data)
        achievement.draw(screen, 50, y_offset)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 50 < mouse_x < 750 and y_offset < mouse_y < y_offset + 50:
                    selected_achievement = achievement
                    set_screen(SCREEN_ACHIEVEMENT_DETAIL)

        y_offset += 100

    back_button.draw(screen)
    for event in events:
        if back_button.is_pressed(event):
            back_button.function()
        if button_back_attempt.is_pressed(event):
            button_back_attempt.function()
        if button_next.is_pressed(event):
            button_next.function()
    if get_number_of_achievements_per_level(1):
        count_of_achievements_1 = font.render(f'1 LEVEL: {get_number_of_achievements_per_level(1)}', True, BUTTON_COLOR)
        screen.blit(count_of_achievements_1, (600, 500))

    if get_number_of_achievements_per_level(2):
        count_of_achievements_2 = font.render(f'2 LEVEL: {get_number_of_achievements_per_level(2)}', True, BUTTON_COLOR)
        screen.blit(count_of_achievements_2, (600, 530))


def draw_achievement_more(events):
    global selected_achievement

    if not selected_achievement:
        set_screen(SCREEN_ACHIEVEMENTS)
        return

    back_button = Button(10, 10, 100, 40, "Назад", lambda: set_screen(SCREEN_ACHIEVEMENTS))
    back_button.draw(screen)

    screen.blit(pygame.transform.scale(selected_achievement.image, (200, 200)), (300, 100))
    attempt = font.render(f'Попытка: {selected_achievement.attempt}', True, BUTTON_COLOR)
    screen.blit(attempt, (WIDTH // 2 - attempt.get_width() + 50, 300))
    name = font.render(f'Название: {selected_achievement.name}', True, BUTTON_COLOR)
    description = font.render(f'Описание: {selected_achievement.description}', True, BUTTON_COLOR)
    level = font.render(f'Уровень: {selected_achievement.level}', True, BUTTON_COLOR)
    screen.blit(name, (WIDTH // 2 - name.get_width() // 2, 350))
    screen.blit(description, (WIDTH // 2 - description.get_width() // 2, 400))
    screen.blit(level, (WIDTH // 2 - 70, 550))
    if selected_achievement.attempt:
        attempt = font.render(f'Попытки: {selected_achievement.attempt}', True, BUTTON_COLOR)
        date = font.render(f'Время получение: {selected_achievement.date}', True, BUTTON_COLOR)
        screen.blit(attempt, (WIDTH // 2 - attempt.get_width() // 2, 450))
        screen.blit(date, (WIDTH // 2 - date.get_width() // 2, 500))

    for event in events:
        if back_button.is_pressed(event):
            back_button.function()


def draw_about_the_authors(events):
    back_button = Button(10, 10, 100, 40, "Назад", lambda: set_screen(SCREEN_MAIN_MENU))
    back_button.draw(screen)

    author1 = font.render('LEVEL 1', True, BUTTON_COLOR)
    screen.blit(author1, (30, 150))
    screen.blit(pygame.transform.smoothscale(GITHUB_IMAGE[0], (150, 150)), (250, 50))
    screen.blit(pygame.transform.smoothscale(TG_IMAGE[0], (150, 150)), (600, 50))
    # author2 = font.render('2 LEVEL', True, BUTTON_COLOR)
    # screen.blit(author2, (30, 300))
    # # screen.blit(pygame.transform.smoothscale(GITHUB_IMAGE[0], (150, 150)), (250, 150))
    # screen.blit(pygame.transform.smoothscale(TG_IMAGE[1], (150, 150)), (600, 250))

    author3 = font.render('LEVEL 2', True, BUTTON_COLOR)
    screen.blit(author3, (30, 300))
    screen.blit(pygame.transform.smoothscale(GITHUB_IMAGE[2], (150, 150)), (250, 250))
    screen.blit(pygame.transform.smoothscale(TG_IMAGE[2], (150, 150)), (600, 250))

    for event in events:
        if back_button.is_pressed(event):
            back_button.function()


def set_screen(screen_name):
    global current_screen
    current_screen = screen_name


def start_screen():
    global current_screen

    clock = pygame.time.Clock()
    running = True

    while running:
        events = pygame.event.get()
        screen.fill(BLACK)
        screen.blit(BACKGROUND_IMG, (0, 0))

        for event in events:
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == lets_go:
                running = False

        if current_screen == SCREEN_MAIN_MENU:
            show_main_menu(events)
        elif current_screen == SCREEN_ACHIEVEMENTS:
            draw_achievements(events)
        elif current_screen == SCREEN_ACHIEVEMENT_DETAIL:
            draw_achievement_more(events)
        elif current_screen == SCREEN_ABOUT_AUTHOR:
            draw_about_the_authors(events)

        pygame.display.update()
        clock.tick(FPS)
