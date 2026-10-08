from sqlalchemy import create_engine,String,Integer
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column


DATABASE_URL="mysql+pymysql://root:@localhost/allenamento"

engine=create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass


class Persona(Base):
    __tablename__="persona"

    id:Mapped[int]= mapped_column(primary_key=True)
    nome:Mapped[str]=mapped_column(String(40),nullable=False)
    eta:Mapped[int]=mapped_column(Integer)

Base.metadata.create_all(engine)



