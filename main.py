from Scene1 import Scene1
from Scene3 import *
from config import *
from final_screen import final_screen
from text import episode_text
from start_screen import start_screen

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Start")

con = sqlite3.connect("db/game.db")
len_db = con.execute("SELECT COUNT (*) FROM level1").fetchone()
attempt = 1 if int(len_db[0]) < 1 else len_db[0]

title_font = pygame.font.SysFont("comicsans", 70)
run = True

while run:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        scene_3 = Scene3(10, WIN, attempt)
        scene_3.gameplay()
        if scene_3.success:
            episode_text(TEXT_1)
        else:
            break

pygame.quit()
