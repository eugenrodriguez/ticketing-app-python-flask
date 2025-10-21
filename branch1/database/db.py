from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    # create tables
    from models.ticket import Ticket
    from models.incidente import Incidente
    db.create_all()
