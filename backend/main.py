from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import engine,Persona

app=FastAPI()

class PersonaInput(BaseModel):
    nome:str
    eta:int
class PersonaUpdate(BaseModel):
    nome: str
@app.get("/persone")
def get_persone():

    with Session(engine) as session:
        stmt=select(Persona)

        persone=session.scalars(stmt).all()

        return persone
@app.post("/persone")
def inserisci_persona(dati:PersonaInput):

    persona=Persona(
        nome=dati.nome,
        eta=dati.eta
    )
    
    with Session(engine) as session:
        
        session.add(persona)
        session.commit()

    return{
        "Persona inserita correttamente"
    }

@app.patch("/persone/{id_persona}")
def modifica_persona(id_persona:int,dati:PersonaUpdate):
    with Session(engine) as session:
        persona=session.get(Persona,id_persona)

        persona.nome=dati.nome

        session.commit()
    return{
        "msg":f"Nome persona con id: {id_persona} modificata con successo"
    }



@app.delete("/persone/{id_persona}")
def elimina_persona(id_persona:int):
    with Session(engine) as session:
        persona=session.get(Persona,id_persona)
        session.delete(persona)
        session.commit()

    return{
        "msg":f"Persona con id {id_persona} eliminata correttamente!"
    }