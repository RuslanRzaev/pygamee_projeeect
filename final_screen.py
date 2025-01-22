from final_achievement import AchievementFinal
from utils import *
import pygame


def final_screen(lives_left, window, current_attempt):
    pygame.display.set_caption('Победа!!!')
    achievements = get_achievements(current_attempt)
    for i in achievements:
        print(i[1], i[2], i[3], i[4], i[5], i[6])

    achievements_objs = []

    for i in achievements:
        achievement_item = AchievementFinal(current_attempt, i[1], i[2], i[3], i[4], i[5], i[6])
        achievements_objs.append(achievement_item)

    VICTORY_SOUND.play(-1)
    run = True

    while run:
        window.blit(pygame.transform.scale(VICTORY_BG, (WIDTH, screen.get_height())), (0, 0))
        window.blit(BUTTON_NEXT, (WIDTH / 2 - BUTTON_NEXT.get_width() / 2, screen.get_height() - 110))
        label = MAIN_FONT.render(f"Вы спасли республику!!!", True, (255, 255, 255))
        window.blit(label, (WIDTH / 2 - label.get_width() / 2, 10))


        label_lives = REGULAR_FONT.render(f"Оставшиеся жизни: {lives_left}", 1, (255, 255, 255))
        label_attempt = REGULAR_FONT.render(f"Текущая попытка: {current_attempt}", 1, (255, 255, 255))

        window.blit(label_lives, (WIDTH / 2 - label_lives.get_width() / 2, 70))

        window.blit(label_attempt, (WIDTH / 2 - label_attempt.get_width() / 2, 120))

        c = 0
        for i in achievements_objs:
            i.draw(screen, WIDTH / 2 - i.bg.get_width() / 2, 190 + 120 * c)
            c += 1


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                VICTORY_SOUND.stop()
                run = False

            if event.type == pygame.QUIT:
                VICTORY_SOUND.stop()
                run = False

        pygame.display.flip()
