#version funcional con SQLalchemy,sqlite,flask de incidente y ticket
#falta documentar los controladores para usar swagger
 
from flask import Flask
from DataBase.db import base, engine
from flasgger import Swagger#, swag_from
#from flask import render_template

from Models.IncidentModel import IncidenteModel
from Models.TicketModel import TicketModel
from Controllers.TicketController import TicketController
from Controllers.IncidenteController import IncidenteController

app = Flask(__name__)

swagger_ticket = Swagger(app, template_file='swagger_master.yml')


with app.app_context():
    base.metadata.create_all(engine)
    
ticket_model = TicketModel()
incidente_model = IncidenteModel()

controller = TicketController(app, ticket_model)
incidente_controller = IncidenteController(app, incidente_model)

@app.route("/")
def index():
    return "hola mundo"


if __name__ == "__main__":
    app.run(debug=True)