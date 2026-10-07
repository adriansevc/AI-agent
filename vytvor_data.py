
import random
import sqlite3

KRAJE = [
    "Bratislavský", "Trnavský", "Trenčiansky", "Nitriansky",
    "Žilinský", "Banskobystrický", "Prešovský", "Košický"
]

# typ starostlivosti: koľko eur stojí jeden poistenec za mesiac
TYPY = {
    "ambulancia": (30, 40),
    "lieky": (25, 35),
    "nemocnica": (50, 70)
}

random.seed(42)

conn = sqlite3.connect("data.db")

conn.execute("DROP TABLE IF EXISTS kraje")
conn.execute("DROP TABLE IF EXISTS naklady")

conn.execute(
    "CREATE TABLE kraje (kraj TEXT, pocet_poistencov INTEGER)"
)

conn.execute(
    "CREATE TABLE naklady (kraj TEXT, mesiac INTEGER, typ TEXT, suma_eur INTEGER)"
)

for kraj in KRAJE:
    poistenci = random.randint(100_000, 250_000)

    conn.execute(
        "INSERT INTO kraje VALUES (?, ?)",
        (kraj, poistenci)
    )

    for mesiac in range(1, 13):
        for typ, (najmenej, najviac) in TYPY.items():
            suma = round(
                poistenci * random.uniform(najmenej, najviac)
            )

            conn.execute(
                "INSERT INTO naklady VALUES (?, ?, ?, ?)",
                (kraj, mesiac, typ, suma)
            )

conn.commit()
conn.close()

print("Hotovo: databáza data.db je vytvorená.")