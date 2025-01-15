from Scene1 import Scene1
from Scene3 import *
from config import *
from level3_objs.text import episode_text
from start_screen import start_screen

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Start")


title_font = pygame.font.SysFont("comicsans", 70)
run = True

while run:
    WIN.blit(BG, (0, 0))
    label = title_font.render("Press [ENTER] to start", True, (255, 255, 255))
    WIN.blit(label, (WIDTH / 2 - label.get_width() / 2, 350))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        start_screen()
        episode_text(TEXT_1)
        scene1 = Scene1(LIVES, WIN)
        scene1.level1_gameplay()
        if scene1.success:
            episode_text(PRE_3_1, PRE_3_2, PRE_3_3)
            scene_3 = Scene3(scene1.lives, WIN)
            scene_3.gameplay()
            if scene_3.success:
                episode_text(TEXT_1)
        else:
            break

pygame.quit()
print('next scene')
