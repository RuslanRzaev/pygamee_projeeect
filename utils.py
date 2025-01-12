import sqlite3

import pygame

con = sqlite3.connect("db/game.db")

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) is not None

def text_bg(label, col=(45, 131, 182)):
    text_bg = pygame.Surface(label.get_size())
    text_bg.fill(col)

    return text_bg

def add_to_db_sqlite(level, attempt, title, desc, img, date, achieved='False'):
    print(level, attempt, title, desc, img, date, achieved)
    try:
        con.execute(f"""INSERT INTO level{str(level)} (attempt, title, description, image, date, achieved)
                    VALUES ('{attempt}', '{title}', '{desc}', '{img}', '{date}', '{achieved}');""").fetchall()
    except sqlite3.IntegrityError:
        con.execute(f"""INSERT INTO level{str(level)} (attempt, title, description, image, date, achieved)
                            VALUES ('{attempt + 1}', '{title}', '{desc}', '{img}', '{date}', '{achieved}');""").fetchall()
    con.commit()


