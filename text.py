import pygame

from config import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def episode_text(text1, text2=None, text3=None):
    pygame.display.set_caption('События между игровыми сюжетами...')
    TEXT_MUSIC.play(-1)
    run = True
    vel = 0.8

    BUTTON_NEXT.set_colorkey(pygame.Color("black"))
    BUTTON_NEXT.convert_alpha()

    text_height = text1.get_height()
    text1.set_colorkey(pygame.Color("black"))
    text1.convert_alpha()

    text_x = WIDTH / 2 - text1.get_width() / 2
    text_y = 700

    if text2 is not None:
        btn_y = text_y + text_height + text2.get_height() + 50
        text2.set_colorkey(pygame.Color("black"))
        text2.convert_alpha()
        if text3 is not None:
            text3.set_colorkey(pygame.Color("black"))
            text3.convert_alpha()
            btn_y = text_y + text_height + text2.get_height() + text3.get_height() + 50
    else:
        btn_y = text_y + text_height

    clock = pygame.time.Clock()


    while run:
        clock.tick(60)
        WIN.blit(BG, (0, 0))
        WIN.blit(text1, (text_x, text_y - vel))
        if text2 is not None:
            WIN.blit(text2, (text_x, (text_y + text_height + 10) - vel))
            if text3 is not None:
                WIN.blit(text3, (text_x, (text_y + text_height +  text2.get_height() + 10) - vel))
        if btn_y > HEIGHT // 2 - 100:
            btn_y -= vel
        WIN.blit(BUTTON_NEXT, (WIDTH / 2 - BUTTON_NEXT.get_width() / 2, btn_y))
        text_y -= vel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                 TEXT_MUSIC.stop()
                 run = False

        pygame.display.flip()
