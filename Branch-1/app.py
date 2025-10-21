#version funcional con SQLalchemy,sqlite,flask de incidente y ticket
#falta documentar los controladores para usar swagger
 
from flask import Flask
from DataBase.db import base, engine
from flasgger import Swagger

from Repository.IncidenteRepository import IncidenteRepository
from Repository.TicketRepository import TicketRepository
from Controllers.TicketController import TicketController
from Controllers.IncidenteController import IncidenteController

app = Flask(__name__)

swagger_ticket = Swagger(app, template_file='swagger_master.yml')


with app.app_context():
    base.metadata.create_all(engine)
    
ticket_model = TicketRepository()
incidente_model = IncidenteRepository()

controller = TicketController(app, ticket_model)
incidente_controller = IncidenteController(app, incidente_model)

@app.route("/")
def index():
    return "hola mundo"


if __name__ == "__main__":
    app.run(debug=True)