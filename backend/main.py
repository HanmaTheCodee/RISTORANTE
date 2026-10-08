from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal
from .models import Utente,Account
from .schemas import RegistrazioneCreate
from pwdlib import PasswordHash



app = FastAPI()


# Gestione della sessione SQLAlchemy
def get_db():
    with SessionLocal() as session:
        yield session




@app.delete("/utenti/{id_utente}", status_code=200)
def elimina_utente(id_utente:int,session:Session=Depends(get_db)):
    utente = session.get(Utente, id_utente)

    if utente is None:

        raise HTTPException(

            status_code=404,

            detail="Utente non trovato"

        )

    session.delete(utente)

    session.commit()

    return {"message": "Utente eliminato correttamente"}



password_hash = PasswordHash.recommended()
#ENDPOINT PER LA REGISTRAZIONE
@app.post("/register",status_code=201)
def registrazione_utente(utente:RegistrazioneCreate,session:Session=Depends(get_db)):

    nuovo_utente=Utente(
        email=utente.email,
        nome=utente.nome,
        cognome=utente.cognome,
        citta=utente.citta,
        cap=utente.cap,
        regione=utente.regione

    )
    
    nuovo_account=Account(
        passHash=password_hash.hash(utente.password)
    )
    nuovo_utente.account=nuovo_account

    try:
        session.add(nuovo_utente)
        session.commit()
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email già registrata o vincolo del database violato"
        )

    return {
        "msg": f"Utente {nuovo_utente.idUtente} registrato correttamente"
    }
