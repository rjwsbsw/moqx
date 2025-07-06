from sqlalchemy import create_engine, text
import os

# Azure SQL Login: saengeradmin, Passwd: a9?w!5HA?UCTZxH
DATABASE_URL=(
    "mssql+pymssql://saengeradmin:a9?w!5HA?UCTZxH"
    "@saengersql.database.windows.net/quizdb01"
)

def test_connection():
    print("🔌 Verbinde mit Datenbank ...")
    engine = create_engine(DATABASE_URL, echo=True, future=True)

    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            print(f"✅ Verbindung erfolgreich! Ergebnis: {result}")
    except Exception as e:
        print("❌ Fehler beim Verbinden:", e)

if __name__ == "__main__":
    test_connection()
