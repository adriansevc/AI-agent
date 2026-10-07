"""AI agent: Gemini odpovedá na otázky o dátach a samo si spúšťa SQL dotazy."""

import sqlite3

from google import genai
from google.genai import types

MODEL = "gemini-3.1-flash"

POKYNY = """Si dátový asistent zdravotnej poisťovne. Odpovedaj po slovensky a stručne.
Čísla si nikdy nevymýšľaj, vždy ich zisti funkciou spusti_sql.
Pod odpoveď pridaj SQL dotaz, ktorý si použil, aby sa dal skontrolovať.
Ak otázka nesúvisí s týmito dátami, zdvorilo odmietni odpovedať.

Databáza (SQLite) obsahuje VYMYSLENÉ dáta za rok 2025:
- kraje(kraj, pocet_poistencov): 8 krajov, názov bez slova "kraj", napríklad "Košický"
- naklady(kraj, mesiac, typ, suma_eur): mesiac je 1 až 12,
  typ je 'ambulancia', 'lieky' alebo 'nemocnica'
"""
def spusti_sql(dotaz: str) -> str:
    """Spustí SQL dotaz nad databázou poisťovne a vráti výsledok.

    Args:
        dotaz: Jeden SQL dotaz SELECT pre SQLite.
    """
    print("SQL:", dotaz)  # v termináli uvidíš, čo si AI spustila

    # mode=ro znamená len na čítanie: AI nemôže nič zmazať ani zmeniť
    conn = sqlite3.connect("file:data.db?mode=ro", uri=True)

    try:
        return str(conn.execute(dotaz).fetchmany(50))
    except sqlite3.Error as chyba:
        return f"Chyba: {chyba}"
    finally:
        conn.close()


def vytvor_chat(client):
    """Vytvorí rozhovor s Gemini, ktoré môže samo volať funkciu spusti_sql."""
    nastavenia = types.GenerateContentConfig(
        system_instruction=POKYNY,
        tools=[spusti_sql],
    )

    return client.chats.create(model=MODEL, config=nastavenia)
if __name__ == "__main__":
    client = genai.Client()  # API kľúč si načíta z premennej GEMINI_API_KEY
    chat = vytvor_chat(client)

    print("Pýtaj sa na dáta poisťovne. Prázdny riadok ukončí program.")

    while True:
        otazka = input("Ty: ")

        if not otazka:
            break

        print("AI:", chat.send_message(otazka).text)