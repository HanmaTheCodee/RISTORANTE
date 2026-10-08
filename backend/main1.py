from fastapi import FastAPI,Depends, HTTPException
from sqlalchemy import select,update,func
from pydantic import BaseModel
from esercizioSQLALCHEMY import get_db,Persona,Session,Ordine
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class addPersona(BaseModel):
    nome:str
    eta:int

class updateNamePersona(BaseModel):
    nome:str

class addOrdine(BaseModel):
    descrizione:str
    prezzo:int
@app.post("/persone",status_code=201 )
def crea_persona(dati:addPersona,session:Session=Depends(get_db)):
    persona=Persona(
        nome=dati.nome,
        eta=dati.eta
    )

    session.add(persona)
    session.commit()

    return{
        "msg":f"Persona inserita corretamente"
    }

@app.get("/persone")
def get_persone(session:Session=Depends(get_db)):

    dato=select(Persona)

    persone=session.scalars(dato).all()

    return persone

@app.get("/persone/{id_persona}")
def get_persona_by_id(id_persona:int,session:Session=Depends(get_db)):

    dato=select(Persona).where(Persona.id==id_persona)

    persona=session.scalar(dato)

    return persona

@app.patch("/persone/{id_persona}")
def modifica_persona(id_persona:int,dato:updateNamePersona,session:Session=Depends(get_db)):


    query=(update(Persona).where(Persona.id==id_persona).values(nome=dato.nome))
    session.execute(query)
    session.commit()

    return{
        "msg":f"Persona con id {id_persona} modificata correttamente"
    }

@app.delete("/persone/{id_persona}" ,status_code=204)
def elimina_persona(id_persona:int,session:Session=Depends(get_db)):

    persona=session.get(Persona,id_persona)
    if persona is None:
        raise HTTPException(
            status_code=404,
            detail="Persona non trovata"
        )
    session.delete(persona)
    session.commit()

    #return{
#    "msg":f"Persona con id {id_persona} eliminata corretamente"
   # }


@app.post("/persone/{id_persona}/ordini")
def crea_ordine(id_persona:int,dato:addOrdine,session:Session=Depends(get_db)):
    persona=session.get(Persona,id_persona)
    ordine=Ordine(
        descrizione=dato.descrizione,
        prezzo=dato.prezzo
    )

    ordine.persona=persona


    session.add(ordine)
    session.commit()

    return{
        "msg":f"Ordine della persona con id {id_persona} aggiunto correttamente"
    }


@app.get("/persone/{id_persona}/ordini")
def ottieni_ordine_persona(id_persona:int,session:Session=Depends(get_db)):

    persona=session.get(Persona,id_persona)

    if persona is None:
        raise HTTPException(
            status_code=404,
            detail="Persona non trovata"
        )
    return persona.ordini

@app.delete("/ordini/{id_ordine}")
def elimina_ordine(id_ordine:int,session:Session=Depends(get_db)):
    ordine=session.get(Ordine,id_ordine)
    if ordine is None:
        raise HTTPException(
            status_code=404,
            detail="Ordine non trovato"
        )
    session.delete(ordine)
    session.commit()
     
    return{
        "msg":f"cancellato ordine con id {id_ordine}"
    }
@app.get("/ordini/costosi")

def get_ordini_costosi(session:Session=Depends(get_db)):

    azione=select(Ordine).where(Ordine.prezzo>=20).order_by(Ordine.prezzo.asc())

    ordini=session.scalars(azione).all()

    return ordini

@app.get("/ordini/costosi/superioriallamedia")
def get_ordini_superiore_alla_media(session:Session=Depends(get_db)):

    media = (
        select(func.avg(Ordine.prezzo))
        .scalar_subquery()
    )

    query = (
        select(Ordine)
        .where(Ordine.prezzo > media)
        .order_by(Ordine.prezzo.desc())
    )



    ordini = session.scalars(query).all()

    return ordini
@app.get("/ordini-con-persone")
def get_ordini_con_persone(
    session: Session = Depends(get_db)
):

    query = (
        select(Ordine, Persona)
        .join(
            Persona,
            Ordine.id_persona == Persona.id
        )
    )

    risultati = session.execute(query).mappings().all()

    return risultati
    