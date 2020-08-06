import sqlite3
import time
from datetime import datetime

conn = sqlite3.connect('memes.db')
c = conn.cursor()
while (True):
    enter = input()
    if (enter == "add"):
        print("Введите описание мема: ")
        description = input()
        print("Введите url мема: ")
        url = input()

        c.execute("INSERT INTO memeTable (url, descr, time) VALUES (?, ?, ?)",
                  (url,
                   description,
                   int(time.time())))
        conn.commit()
        print('Добавлено!')

    elif (enter == "all"):
        c.execute("SELECT * FROM memeTable")
        result = c.fetchall()
        for line in result:
            print("id: ", line[0])
            print("url: ", line[1])
            print("descr: ", line[2])
            print(line[3])

    elif (enter == "delete"):
        print('Введите id мема который выхотите удалить: ')
        memeID = int(input())
        c.execute("DELETE FROM memeTable WHERE id=?", [memeID])
        print("Удалено!")
        conn.commit()
    else:
        print("Такой команды нет!")

conn.commit()
conn.close()
