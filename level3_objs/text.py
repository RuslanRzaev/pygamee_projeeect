import math

import pygame
from config import *
from utils import collide

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def episode_text(text_img, text2=None, text3=None):
    TEXT_MUSIC.play(-1)

    run = True

    text_height = text_img.get_height()

    text = pygame.transform.scale(text_img, (text_img.get_width(), HEIGHT))

    text_x = WIDTH / 2 - text.get_width() / 2
    text_y = 700

    if text2 is not None and text3 is not None:
        btn_y = text_y + text_height + text2.get_height() + text3.get_height() + 150
    else:
        btn_y = text_y + text_height + 300

    vel = 1.2

    clock = pygame.time.Clock()


    while run:
        clock.tick(60)
        WIN.blit(BG, (0, 0))
        WIN.blit(text, (text_x, text_y - vel))
        if text2 is not None and text3 is not None:
            WIN.blit(text2, (text_x, (text_y + text_height + 180) - vel))
            WIN.blit(text3, (text_x, (text_y + text_height +  text2.get_height() + 180) - vel))
        if btn_y > HEIGHT // 2 - 100:
            btn_y -= vel
        WIN.blit(BUTTON_NEXT, (WIDTH / 2 - BUTTON_NEXT.get_width() / 2, btn_y))
        text_y -= vel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                 TEXT_MUSIC.stop()
                 run = False


        pygame.display.flip()
