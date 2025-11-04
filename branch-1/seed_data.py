from database.db import init_db, get_session
from models.ticket import Ticket
from models.incidente import Incidente
from sqlalchemy import text


def insertar_datos_hardcodeados():
    init_db()
    session = get_session()
    
    print("Insertando datos hardcodeados...")
    
    conn = session.connection()
    
    conn.execute(text("DELETE FROM clientes"))
    clientes = [
        (1, "Juan Pérez", "juan@email.com", "555-0001", "Calle Falsa 123"),
        (2, "María García", "maria@email.com", "555-0002", "Av. Siempre Viva 456"),
        (3, "Carlos López", "carlos@email.com", "555-0003", "Calle Principal 789"),
    ]
    for cliente in clientes:
        conn.execute(text(
            "INSERT OR REPLACE INTO clientes (id, nombre, email, telefono, direccion) "
            "VALUES (:id, :nombre, :email, :telefono, :direccion)"
        ), {"id": cliente[0], "nombre": cliente[1], "email": cliente[2], 
            "telefono": cliente[3], "direccion": cliente[4]})
    print(f" {len(clientes)} clientes insertados")
    
    conn.execute(text("DELETE FROM empleados"))
    empleados = [
        (1, "Pedro Técnico", "Técnico", "Soporte Técnico"),
        (2, "Ana Operadora", "Operador", "Atención Telefónica"),
        (3, "Luis Técnico", "Técnico", "Soporte Técnico"),
    ]
    for empleado in empleados:
        conn.execute(text(
            "INSERT OR REPLACE INTO empleados (id, nombre, categoria, rol) "
            "VALUES (:id, :nombre, :categoria, :rol)"
        ), {"id": empleado[0], "nombre": empleado[1], "categoria": empleado[2], "rol": empleado[3]})
    print(f" {len(empleados)} empleados insertados")
    
    conn.execute(text("DELETE FROM equipos"))
    equipos = [
        (1, "Notebook Dell Inspiron", "Computadora", "Dell", "Inspiron 15", "SN12345"),
        (2, "Impresora HP LaserJet", "Impresora", "HP", "LaserJet Pro", "SN67890"),
        (3, "Monitor Samsung 24", "Monitor", "Samsung", "S24F350", "SN11111"),
    ]
    for equipo in equipos:
        conn.execute(text(
            "INSERT OR REPLACE INTO equipos (id, descripcion, categoria, marca, modelo, nro_serie) "
            "VALUES (:id, :desc, :cat, :marca, :modelo, :serie)"
        ), {"id": equipo[0], "desc": equipo[1], "cat": equipo[2], 
            "marca": equipo[3], "modelo": equipo[4], "serie": equipo[5]})
    print(f" {len(equipos)} equipos insertados")
    
    conn.execute(text("DELETE FROM servicios"))
    servicios = [
        (1, "Reparación de Hardware"),
        (2, "Instalación de Software"),
        (3, "Mantenimiento Preventivo"),
    ]
    for servicio in servicios:
        conn.execute(text(
            "INSERT OR REPLACE INTO servicios (id, nombre) VALUES (:id, :nombre)"
        ), {"id": servicio[0], "nombre": servicio[1]})
    print(f" {len(servicios)} servicios insertados")
    
    session.commit()


def insertar_tickets_con_incidentes():
    session = get_session()
    
    print(" Insertando tickets con incidentes (relación 1:N)...")
    
    session.query(Incidente).delete()
    session.query(Ticket).delete()
    session.commit()
    
    ticket1 = Ticket(
        cliente_id=1,
        servicio_id=1,
        equipo_id=1,
        empleado_id=1,
        estado="Abierto"
    )
    ticket1.incidentes.append(Incidente(
        descripcion="Pantalla no enciende",
        categoria="Hardware",
        prioridad="Alta",
        ticket_id=0  
    ))
    ticket1.incidentes.append(Incidente(
        descripcion="Batería no carga",
        categoria="Hardware",
        prioridad="Media",
        ticket_id=0
    ))
    session.add(ticket1)
    
    ticket2 = Ticket(
        cliente_id=2,
        servicio_id=2,
        equipo_id=2,
        empleado_id=2,
        estado="En Progreso"
    )
    ticket2.incidentes.append(Incidente(
        descripcion="Sistema operativo no inicia",
        categoria="Software",
        prioridad="Crítica",
        ticket_id=0
    ))
    session.add(ticket2)
    
    ticket3 = Ticket(
        cliente_id=3,
        servicio_id=3,
        equipo_id=3,
        empleado_id=3,
        estado="Abierto"
    )
    ticket3.incidentes.append(Incidente(
        descripcion="Conexión a red intermitente",
        categoria="Red",
        prioridad="Media",
        ticket_id=0
    ))
    ticket3.incidentes.append(Incidente(
        descripcion="No detecta WiFi",
        categoria="Red",
        prioridad="Alta",
        ticket_id=0
    ))
    ticket3.incidentes.append(Incidente(
        descripcion="Velocidad de descarga lenta",
        categoria="Red",
        prioridad="Baja",
        ticket_id=0
    ))
    session.add(ticket3)
    
    session.commit()
    
    print(f" 3 tickets creados con total de 6 incidentes")
    print(f"   - Ticket 1: 2 incidentes (Hardware)")
    print(f"   - Ticket 2: 1 incidente (Software)")
    print(f"   - Ticket 3: 3 incidentes (Red)")


def main():
    """Ejecuta la inserción de datos."""
    print("=" * 60)
    print(" Iniciando inserción de datos de prueba")
    print("=" * 60)
    
    try:
        insertar_datos_hardcodeados()
        insertar_tickets_con_incidentes()
        
        print("\n" + "=" * 60)
        print(" ¡Datos insertados exitosamente!")
        print("=" * 60)
        print("\n Resumen:")
        print("   - 3 clientes hardcodeados")
        print("   - 3 empleados hardcodeados")
        print("   - 3 equipos hardcodeados")
        print("   - 3 servicios hardcodeados")
        print("   - 3 tickets con SQLAlchemy")
        print("   - 6 incidentes con SQLAlchemy (relación 1:N)")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n Error al insertar datos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
