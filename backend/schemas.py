from pydantic import BaseModel, EmailStr, Field


class RegistrazioneCreate(BaseModel):
    email: EmailStr
    nome: str = Field(min_length=1, max_length=50)
    cognome: str = Field(min_length=1, max_length=50)
    citta: str = Field(min_length=1, max_length=100)
    regione: str = Field(min_length=1, max_length=100)
    cap: str = Field(min_length=1, max_length=25)
    password:str=Field(min_length=8)

class LoginCreate(BaseModel):
    email:EmailStr
    password:str

class PiattoOrdineCreate(BaseModel):
    idPiatto:int
    quantita:int=Field(gt=0)

class OrderCreate(BaseModel):
    piatti:list[PiattoOrdineCreate]
    