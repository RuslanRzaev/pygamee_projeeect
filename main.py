from Scene1 import Scene1
from Scene2 import *
from config import *
from final_screen import final_screen
from text import episode_text
from start_screen import start_screen

pygame.font.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Старт")

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
        #start_screen()
        episode_text(START_TEXT_1, START_TEXT_2)
        scene1 = Scene1(LIVES, WIN, attempt)
        scene1.level1_gameplay()
        if scene1.success:
            episode_text(PRE_3_1, PRE_3_2, PRE_3_3)
            scene2 = Scene2(scene1.lives, WIN, attempt)
            scene2.gameplay()
            if scene2.success:
                final_screen(scene2.lives, WIN, attempt)

pygame.quit()
