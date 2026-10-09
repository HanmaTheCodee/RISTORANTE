import secrets
from pathlib import Path

def genera_chiave():

    percorso = Path(__file__).resolve().parent.parent / ".env"

    if percorso.exists():

        contenuto = percorso.read_text()

        if any(

            riga.strip().startswith("JWT_SECRET_KEY=")

            for riga in contenuto.splitlines()

        ):

            print("La chiave JWT esiste già.")

            return

    chiave = secrets.token_hex(32)

    with percorso.open("a") as file:

        file.write(f"\nJWT_SECRET_KEY={chiave}\n")

    print("Chiave JWT generata correttamente.")

if __name__ == "__main__":

    genera_chiave()