import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# import pymssql.exceptions
import sqlalchemy.exc
from .sqlalchemy_model import Base

# Azure SQL Login: saengeradmin, Passwd: a9?w!5HA?UCTZxH
if os.getenv("DATABASE_URL", None):
    DATABASE_URL=os.getenv("DATABASE_URL")
elif os.getenv("SQL_USER", None):
    DATABASE_URL = (
        f"mssql+pymssql://{os.getenv('SQL_USER')}:{os.getenv('SQL_PASSWORD')}"
        f"@{os.getenv('SQL_SERVER')}/{os.getenv('SQL_DATABASE')}"
        "?charset=utf8&timeout=30"
    )
else:
    raise Exception("Keine Datenbank-URL und keine DB-Account-Environment gefunden.")
    DATABASE_URL=(  "mssql+pymssql://saengeradmin:a9?w!5HA?UCTZxH"
                    "@saengersql.database.windows.net:1433/quizdb01"
                    "?charset=utf8&timeout=30"
                    )

print(DATABASE_URL)

OperationalError = sqlalchemy.exc.OperationalError

def get_engine(path=DATABASE_URL):
    return create_engine(path, echo=False, future=True)

def create_db(engine):
    Base.metadata.create_all(bind=engine)

def get_session(engine):
    Session = sessionmaker(bind=engine, future=True)
    return Session()
