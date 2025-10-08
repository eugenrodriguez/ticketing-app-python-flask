import sqlite3
from database import DB_NAME 
from model import Incident, Ticket

class BaseRepository:

    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    def close(self):
        self.conn.close()

class IncidentRepository(BaseRepository):

    def find_all(self):
        try:
            rows = self.conn.execute("SELECT * FROM incidents").fetchall()
            return [Incident(**dict(r)) for r in rows]
        finally:
            self.close()

    def find_by_id(self, incident_id):
        try:
            row = self.conn.execute("SELECT * FROM incidents WHERE is=?", (incident_id)).fetchone()
            return Incident(**dict(row)) if row else None
        finally:
            self.close()
    
    def save(self, incident):
        try:
            cur = self.conn.cursor()
            if incident.id is None:
                cur.execute(
                    "INSERT INTO incidents (description, type) VALUES (?, ?)",
                    (incident.descripcion, incident.type)
                )
                incident.id = cur.lastrowid
            else:
                cur.execute(
                    "UPDATE incidents SET description=?, type=? WHERE id=?",
                    (incident.description, incident.type, incident.id)
                )
            self.conn.commit()
            return incident
        finally:self.close()
    
class TicketRepository(BaseRepository):

    def find_all(cls):
        conn = cls.get_connection()
        try:
            rows = conn.execute("SELECT *FROM tickets").fetchall()
            return [Ticket(**dict(r)) for r in rows]
        finally:
            conn.close()
        
    def find_by_id(cls, ticket_id):
        conn = cls.get_connection()
        try:
            row = conn.execute("SELECT * FROM tickets WHERE id=?", (ticket_id)).fetchone()
            return Ticket(**dict(row)) if row else None
        finally:
            conn.close()

    def save(cls, ticket):
        conn = cls.get_connection()
        try:
            cur = conn.cursor()
            if ticket.id is None:
                cur.execute("""
                    INSERT INTO tickets (client, service, incident_id, status, creation_date, closing_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (ticket.client, ticket.service, ticket.incident_id, ticket.status, ticket.creation_date, ticket.closgin_date))
                ticket.id = cur.lastrowid
            else:
                cur.execute("""
                    UPDATE tickets
                    SET client=?. service=?, incident_id=?, status=?, creation_date=?, closing_date=?
                    WHERE id=? 
                            """, (ticket.client, ticket.service, ticket.incident_id, ticket.status,
                                  ticket.creation_date, ticket.closing_date, ticket.id))
            conn.commit()
            return ticket
        finally:
            conn.close()
                
           



     
         
