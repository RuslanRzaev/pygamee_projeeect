from Scene3 import *
from config import *
from level3_objs.text import episode_text

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Start")


title_font = pygame.font.SysFont("comicsans", 70)
run = True

while run:
    len_db = utils.con.execute("select count(*) from level3").fetchone()
    WIN.blit(BG, (0, 0))
    label = title_font.render("Press [ENTER] to start", True, (255, 255, 255))
    WIN.blit(label, (WIDTH / 2 - label.get_width() / 2, 350))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                episode_text(PRE_3_1, PRE_3_2, PRE_3_3)
                scene_3 = Scene3(LIVES, WIN)
                scene_3.gameplay()
                if scene_3.success:
                    episode_text(TEXT_1)
            if event.type == pygame.QUIT:
                run = False

pygame.quit()
print('next scene')
