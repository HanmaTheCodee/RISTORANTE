from sqlalchemy import create_engine,select,update,func,ForeignKey,String,Integer

from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,Session,relationship


DATABASE_URL="mysql+pymysql://root:@localhost/allenamento"

engine=create_engine(DATABASE_URL)

def get_db():
    with Session(engine) as session:
        yield session

class Base(DeclarativeBase):
    pass

class Persona(Base):
    __tablename__="persona"

    id_eta:Mapped[int]=mapped_column(Integer,primary_key=True)
    nome:Mapped[str]=mapped_column(String(40),nullable=False)
    eta:Mapped[int]=mapped_column(Integer,nullable=False)
    ordini:Mapped[list["Ordine"]]=relationship(back_populates="persona")

class Ordine(Base):
    __tablename__="ordine"

    id :Mapped[int]=mapped_column(Integer,primary_key=True)
    descrizione:Mapped[str]=mapped_column(String(255),nullable=False)
    prezzo:Mapped[int]=mapped_column(Integer,nullable=False)
    id_persona:Mapped[int]=mapped_column(ForeignKey("persona.id"))
    persona:Mapped["Persona"]=relationship(back_populates="ordini")

#prendi tutte le tabelle descritte nei model che derivano da Base e crea nel database quelle che ancora non esistono
Base.metadata.create_all(engine)