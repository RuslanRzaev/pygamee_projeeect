import pygame

from config import *

WIN = pygame.display.set_mode((WIDTH, HEIGHT))


def episode_text(text1, text2=None, text3=None):
    pygame.display.set_caption('События между игровыми сюжетами...')
    TEXT_MUSIC.play(-1)
    run = True
    text_run = True

    text_height = text1.get_height()
    text1.set_colorkey(pygame.Color("black"))
    text1.convert_alpha()

    text_x = WIDTH / 2 - text1.get_width() / 2
    text_y = 700

    if text2 is not None:
        txt_next_y = text_y + text_height + text2.get_height() + 50
        text2.set_colorkey(pygame.Color("black"))
        text2.convert_alpha()
        if text3 is not None:
            text3.set_colorkey(pygame.Color("black"))
            text3.convert_alpha()
            txt_next_y = text_y + text_height + text2.get_height() + text3.get_height() + 50
    else:
        txt_next_y = text_y + text_height

    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        WIN.blit(BG, (0, 0))

        if not text_run:
            WIN.blit(RESUME, (20, 20))
            vel = 0
        else:
            WIN.blit(PAUSE, (20, 20))
            vel = 0.45

        WIN.blit(text1, (text_x, text_y - vel))
        if text2 is not None:
            WIN.blit(text2, (text_x, (text_y + text_height + 10) - vel))
            if text3 is not None:
                WIN.blit(text3, (text_x, (text_y + text_height +  text2.get_height() + 10) - vel))
        if txt_next_y > HEIGHT // 2:
            txt_next_y -= vel
        WIN.blit(TEXT_NEXT, (WIDTH / 2 - TEXT_NEXT.get_width() / 2, txt_next_y))
        WIN.blit(BUTTON_NEXT, (WIDTH - 110, 10))
        check_rect = pygame.Rect(WIDTH / 2 - TEXT_NEXT.get_width() / 2, txt_next_y, TEXT_NEXT.get_width(),
                                 TEXT_NEXT.get_height())
        check_rect_next = pygame.Rect(WIDTH - 110, 10, BUTTON_NEXT.get_width(),
                                 BUTTON_NEXT.get_height())
        text_y -= vel

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_rect.collidepoint(pygame.mouse.get_pos()):
                    TEXT_MUSIC.stop()
                    run = False
                if PAUSE.get_rect().collidepoint(pygame.mouse.get_pos()):
                    text_run = not text_run
                    if text_run:
                        pygame.mixer.unpause()
                    else:
                        pygame.mixer.pause()
                if check_rect_next.collidepoint(pygame.mouse.get_pos()):
                    TEXT_MUSIC.stop()
                    run = False

        pygame.display.flip()
