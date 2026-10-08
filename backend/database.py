from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,Mapped,sessionmaker


DATABASE_URL="mysql+pymysql://root:@localhost/ristorante"

engine=create_engine(DATABASE_URL)

class Base(DeclarativeBase):
    pass

SessionLocal=sessionmaker(bind=engine)

def get_db():
    with SessionLocal() as session:
        yield session



