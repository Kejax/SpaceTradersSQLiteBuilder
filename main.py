import sqlite3
import requests
import time

api_url = "https://api.spacetraders.io/v2/"


def open_database():
    return sqlite3.connect("spacetraders.sqlite")


def build_systems_table():

    db = open_database()
    db.execute("DROP TABLE IF EXISTS systems")
    db.execute("CREATE TABLE systems (symbol TEXT UNIQUE, sectorSymbol TEXT, type TEXT, x INTEGER, y INTEGER)")
    db.commit()

    f = 0

    for i in range(1, 430):

        time.sleep(0.5)

        systems = requests.get(api_url + f"/systems?page={i}&limit=20").json()["data"]

        cursor = db.cursor()

        for system in systems:

            f += 1
            print(f)

            cursor.execute(
                "INSERT OR IGNORE INTO systems (symbol, sectorSymbol, type, x, y) VALUES (?, ?, ?, ?, ?)",
                (
                    system["symbol"],
                    system["sectorSymbol"],
                    system["type"],
                    system["x"],
                    system["y"]
                )
            )

            db.commit()

        cursor.close()

    db.close()

build_systems_table()
