from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import SessionLocal
from .models import Utente,Account,Ordine,Piatto
from .schemas import RegistrazioneCreate,LoginCreate,PiattoOrdineCreate,OrderCreate
from pwdlib import PasswordHash

import jwt
import os

from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

#integrazione JWT

percorso_env = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(percorso_env)

SECRET_KEY = os.environ["JWT_SECRET_KEY"]

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def crea_access_token(id_utente: int):

    scadenza = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(id_utente),
        "exp": scadenza
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
security = HTTPBearer()
# Gestione della sessione SQLAlchemy
def get_db():
    with SessionLocal() as session:
        yield session
def verifica_token(token: str):

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
            options={"require": ["sub", "exp"]}
        )

        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401,
            detail="Token scaduto"
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Token non valido"
        )

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_db)
):
    token = credentials.credentials

    payload = verifica_token(token)

    id_utente = payload.get("sub")

    try:
        id_utente = int(id_utente)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="ID utente non valido"
        )

    utente = session.get(Utente, id_utente)

    if utente is None:
        raise HTTPException(
            status_code=401,
            detail="Utente non trovato"
        )

    return utente

    
app = FastAPI()







@app.delete("/auth/utenti/{id_utente}", status_code=200)
def elimina_utente(id_utente:int,
                   session:Session=Depends(get_db),
                   utente_corrente:Utente=Depends(get_current_user)
                   ):

    

    if utente_corrente.idUtente != id_utente:

        raise HTTPException(

            status_code=403,

            detail="Non puoi eliminare un altro utente"

        )
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
@app.post("/auth/register",status_code=201)
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


#ENDPOINT LOGIN 
@app.post("/auth/login",status_code=200)
def login_utente(utente:LoginCreate,session:Session=Depends(get_db)):
    vecchio_utente = session.scalar(

    select(Utente).where(Utente.email == utente.email)

)
    if vecchio_utente is None:
        raise HTTPException (
            status_code=401,
            detail="Credenziali non valide"
        )
    
    account=vecchio_utente.account

    if account is None:
        raise HTTPException(
            status_code=401,
            detail="Credenziali non valide"
        )
    
    if password_hash.verify(
        utente.password,account.passHash
    ) is False:
        raise HTTPException(
            status_code=401,
            detail="Credenziali non valide"
        )
    
    access_token = crea_access_token(vecchio_utente.idUtente)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@app.get("/auth/me", status_code=200)
def profilo_utente(
    utente: Utente = Depends(get_current_user)
):
    return {
        "idUtente": utente.idUtente,
        "nome": utente.nome,
        "cognome": utente.cognome,
        "email": utente.email
    }




    
