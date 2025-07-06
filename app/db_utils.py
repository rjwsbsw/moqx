from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_model import Base

# Azure SQL Login: saengeradmin, Passwd: a9?w!5HA?UCTZxH
DATABASE_URL=(
    "mssql+pymssql://saengeradmin:a9?w!5HA?UCTZxH"
    "@saengersql.database.windows.net/quizdb01"
)

def get_engine(path=DATABASE_URL):
    return create_engine(path, echo=False, future=True)

def create_db(engine):
    Base.metadata.create_all(bind=engine)

def get_session(engine):
    Session = sessionmaker(bind=engine, future=True)
    return Session()
