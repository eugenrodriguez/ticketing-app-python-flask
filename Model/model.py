from dataclasses import dataclass
from datetime import datetime 
from typing import Optional

@dataclass
class Incident:
    id: int
    description: str
    type: str

@dataclass
class Ticket:
    id: int
    customer: str #hc
    service: str #hc
    incident_id: int
    status: str = "Abierto"
    creation_date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    closing_date: Optional[str] = None