import textwrap
from config import *
import pygame

from utils import load_image

TEXT_DIALOG = {'ja:Это килдык! О, рыба губер!': '18_20', 'kwaigoi:За что тебя изгнали Джа Джа?': '21_22', 'ja:Это рассказывать долго... Но если короче говориии... Моя, неуклюжий': '23_29', 'kwaigoi: Изгнали за то что ты неклюжий?': '24_31',
               'ja: Нуэаа.. Да можно и так говорить!': '32_34', 'ja: Моя причиня один-два маленький, но плохой авария. Раньше BOOM догаср и разбеха для барбоса и изгнать:((': '47_57', 'ja: ААААААААААААААА!! Страшные звуки*': '60_62',
               'ja: БОЛЬШОЙ РЫБА ГУБЕР! ЗУБАСТЫЙ!!! Страшные звуки*' : '62_76', 'obi_van: Всегда найдется рыба крупней': '76_78', 'ja: Моя думает лучше вернись! Страшные звуки* + Политика': '78_128',
               'ja: Куда теперя??': '128_130', 'obi_van: Не волнуйся, сила укажет': '130_133', 'ja: Оо (макси класс) твоя сила, но дело пахнет керосина': '133_140',
               'kwaigoi: Снизилась мощность': '140_149', 'ja: Наша тут умираааать((((': '149_151', 'obi_van: Успокойся, это ещё не беда': '151_153',
               'ja: ВОТ ТАК!! МОНСТРЫ ТА МА! НАША ТОНУТЬ СОВСЕМ! ЭТА ДВИГАТЕЛЬ СДОХЛА!!!!!!! А ТЫ ГОВОРИТЬ ЭТО ЕЩЁ НЕ ЕСТЬ БЕДА!!': '153_164',
               'kwaigoi: Готово!': '164_166', 'ja: ААААААААААА! МОНСТРЫ! + СТРАШНЫЕ ЗВУКИ': '166_176', 'obi_van: Перестань! Ну это слишком! + страшные звуки': '166_195',
               'obi_van: Курс вон на то возвышение!': '196_250'}




def parsed_dialog():
    parsed_dialogs = []
    for key, value in TEXT_DIALOG.items():
        character, text = key.split(':', 1)
        start, end  = map(int, value.split('_'))
        parsed_dialogs.append({"character": character, "text": text, "start": start, "end": end})
    return parsed_dialogs

def generate_dialogs(TIME_GAME, screen):
    for dialog in parsed_dialog():
        if dialog['start'] <= TIME_GAME <= dialog['end']:
            lines = textwrap.wrap(dialog['text'], 40)
            rect_text = pygame.draw.rect(screen, pygame.Color('gray'), (50, HEIGHT - 120, WIDTH - 100, 100))
            screen.blit(character_images[dialog['character']], (60, rect_text.center[1] - 50))
            y = rect_text.top + 10
            for line in lines:
                text = pygame.font.Font(None, 32).render(line, True, pygame.Color('white'))
                screen.blit(text, (150, y))
                y += 30
            break

character_images = {
        'ja': pygame.transform.smoothscale(load_image('ja.png', -1), (80, 80)),
        'kwaigoi': pygame.transform.smoothscale(load_image('kwaigoi.png', -1), (80, 80)),
        'obi_van': pygame.transform.smoothscale(load_image('obi_van.png', -1), (80, 80)),
    }

