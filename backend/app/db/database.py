from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://ai_user:ai_password@localhost:5432/ai_db"

#creates a SQLAlchemy Engine.
engine = create_engine(DATABASE_URL)

# SessionLocal is a factory for creating new Session objects. It is configured to use the engine created above, 
# and it has autoflush and autocommit set to False. This means that changes made in a session will not be automatically flushed to the database, and transactions will not be automatically committed.
SessionLocal = sessionmaker(
    bind = engine,
    autoflush = False,
    autocommit = False,
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()