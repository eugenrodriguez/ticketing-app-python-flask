from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

db_url = "sqlite:///TicketDB.db"

engine = create_engine(db_url, echo=True)
base = declarative_base()
Sesion = sessionmaker(bind=engine)